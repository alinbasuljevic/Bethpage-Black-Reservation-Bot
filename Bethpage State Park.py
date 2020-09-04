import requests, time, json
from bs4 import BeautifulSoup as bs

s = requests.Session()
print ('Starting Bethpage State Park Reservation Bot...')
#desired_time = input('Enter Desired Time Hour: ')
players = 4
holes = 18
course = 'Bethpage Black Course'
print ('-----------------------------------------------')
print ('Accessing user account...')
login_url = 'https://foreupsoftware.com/index.php/api/booking/users/login'
times_available_url = 'https://foreupsoftware.com/index.php/api/booking/times?time=all&date=09-05-2020&holes=18&players=4&booking_class=2136&schedule_id=2431&schedule_ids%5B%5D=0&schedule_ids%5B%5D=2517&schedule_ids%5B%5D=2431&schedule_ids%5B%5D=2433&schedule_ids%5B%5D=2539&schedule_ids%5B%5D=2538&schedule_ids%5B%5D=2434&schedule_ids%5B%5D=2432&schedule_ids%5B%5D=2435&specials_only=0&api_key=no_limits'


headers = {
    'Accept': '*/*',
    'Accept-Encoding': 'gzip, deflate, br',
    'Accept-Language': 'en-US,en;q=0.9',
    'Api-key': 'no_limits',
    'Connection': 'keep-alive',
    'Host': 'foreupsoftware.com',
    'Origin': 'https://foreupsoftware.com',
    'Referer': 'https://foreupsoftware.com/index.php/booking/19765/2431',
    'Sec-Fetch-Dest': 'empty',
    'Sec-Fetch-Mode': 'cors',
    'Sec-Fetch-Site': 'same-origin',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.135 Safari/537.36',
    'X-NewRelic-ID': 'VQ8GUFFQGwUFVlBQBAQPUw==',
    'X-Requested-With': 'XMLHttpRequest'
    }

login_form_data = {
    'username': 'shkreli7@gmail.com',
    'password': 'Newyorkcity1234!',
    'booking_class_id': '2136',
    'api_key': 'no_limits',
    'course_id': '19765'
    }

login_request = s.post(login_url, data=login_form_data, headers=headers)

if login_request.status_code == 200:
    print ('Logged in!')
    print ('Finding Open Reservations for {}...'.format(course))
else:
    print (login_request.status_code)
while True:
    try:
        available_times = s.get(times_available_url, headers=headers).json()
        #beginning_time = desired_time_range.split('-')[0]
        #ending_time = desired_time_range.split('-')[1]
        #print (available_times)
        for item in available_times:
            print (item['time'])
            date = item['time'].split(' ')[0]
            time = item['time'].split(' ')[1]
            hours = int(time.split(':')[0])
            minutes = int(time.split(':')[1])
            if hours > 12:
                setting = "PM"
                hours -= 12
            else:
                setting = "AM"

            normal_time = '{}:{} {}'.format(hours, minutes, setting)
            #print (normal_time)
            
            course_name = item['schedule_name']
            num_of_players = item['available_spots']
            if int(num_of_players)  == int(players):
                reservation_payload = {
                    'time': item['time'],
                    'holes': item['holes'],
                    'players': num_of_players,
                    'carts': 'false',
                    'schedule_id': item['schedule_id'],
                    'course_id': item['course_id'],
                    'booking_class_id': item['booking_class_id'],
                    'duration': '1'
                    }
                print ('Found Slot: [Course: {}][Number of Players: {}][Tee Time: {}]'.format(course_name, num_of_players, normal_time))
                print ('Generated Reservation Payload!')
                
                pending_reservation_url = 'https://foreupsoftware.com/index.php/api/booking/pending_reservation'
                initial_reservation_request = s.post(pending_reservation_url, data=reservation_payload, headers=headers).json()
                #print (initial_reservation_request)
                if initial_reservation_request['success'] == True:
                    print ('Reservation reserved for 5 minutes! Finalizing confirmation now...')
                    reservation_id = initial_reservation_request['reservation_id']
                    sitekey = '6LeQqCIUAAAAAI8nAaJahskkE6mNTI9cBBRseaFO'
                    API_KEY = '8ababd23c4f53dc37e7a9044391d479f'
                    challenge_url = 'https://foreupsoftware.com/index.php/booking/19765/2431#/teetimes'
                    captcha_loop = True
                    while captcha_loop:
                        captcha_id = s.post("http://2captcha.com/in.php?key={}&method=userrecaptcha&googlekey={}&pageurl={}".format(API_KEY, sitekey, challenge_url)).text.split('|')[1]
                        recaptcha_answer = s.get("http://2captcha.com/res.php?key={}&action=get&id={}".format(API_KEY, captcha_id)).text
                        while 'CAPCHA_NOT_READY' in recaptcha_answer:
                            recaptcha_answer = s.get("http://2captcha.com/res.php?key={}&action=get&id={}".format(API_KEY, captcha_id)).text
                        try:
                            print (item['course_id'])
                            recaptcha_answer = recaptcha_answer.split('|')[1]
                            print (recaptcha_answer)
                            final_reservation_conf_payload = {
                                'airQuotesCart': [{'type': "item", 'description': "Green Fee", 'price': 31, 'quantity': num_of_players, 'subtotal': int(num_of_players) * 31}],
                                'allow_mobile_checkin': 0,
                                'available_duration': 'null',
                                'available_spots': num_of_players,
                                'booking_class_id': '2138',
                                'booking_fee_per_person': False,
                                'booking_fee_price': False,
                                'booking_fee_required': False,
                                'captchaid': recaptcha_answer,
                                'cart_fee': False,
                                'cart_fee_tax': 0,
                                'cart_fee_tax_rate': False,
                                'carts': False,
                                'course_id': item['course_id'],
                                'course_name': "Bethpage State Park",
                                'customer_message': "",
                                'details': "",
                                'discount': 0,
                                'discount_percent': 0,
                                'duration': 1,
                                'estimatedTax': 0,
                                'foreup_discount': False,
                                'foreup_trade_discount_information': '[]',
                                'foreup_trade_discount_rate': 0,
                                'green_fee': 31,
                                'green_fee_tax': 0,
                                'green_fee_tax_rate': False,
                                'group_id': False,
                                'guest_cart_fee': False,
                                'guest_cart_fee_tax': 0,
                                'guest_cart_fee_tax_rate': False,
                                'guest_green_fee': 31,
                                'guest_green_fee_tax': 0,
                                'guest_green_fee_tax_rate': False,
                                'has_special': False,
                                'hide_prices': True,
                                'holes': 18,
                                'increment_amount': 'null',
                                'max_players': 4,
                                'merchantNotSupported': True,
                                'min_players': 1,
                                'minimum_players': 1,
                                'paid_player_count': 0,
                                'pay_carts': False,
                                'pay_online': "no",
                                'pay_players': num_of_players,
                                'pay_subtotal': int(num_of_players) * 31,
                                'pay_total': int(num_of_players) * 31,
                                'pending_reservation_id': reservation_id,
                                'player_list': False,
                                'players': num_of_players,
                                'preTaxSubtotal': int(num_of_players) * 31,
                                'promo_code': "",
                                'promo_discount': 0,
                                'purchased': False,
                                'rate_type': "walking",
                                'require_credit_card': 0,
                                'schedule_id': item['schedule_id'],
                                'schedule_name': course_name,
                                'show_course_name': False,
                                'special_discount_percentage': 0,
                                'special_id': False,
                                'subtotal': int(num_of_players) * 31,
                                'teesheet_holes': holes,
                                'teesheet_id': item['teesheet_id'],
                                'time': item['time'],
                                'total': int(num_of_players) * 31,
                                'trade_available_players': '0',
                                'trade_min_players': '8',
                                }
                            #print (final_reservation_conf_payload)
                            
                            final_url = 'https://foreupsoftware.com/index.php/api/booking/users/reservations'
                            final_reservation = s.post(final_url, json=final_reservation_conf_payload, headers=headers)
                            json_data = json.loads(final_reservation.text)
                            #print (json_data)
                            if final_reservation.status_code == 200:
                                print ('-------------------------------------')
                                print ('Successfully Reserved Tee Time Bitch! Peep the details below!')
                                print ('Teetime_ID: {}'.format(json_data['teetime_id']))
                                print ('Reservation Time: {}'.format(json_data['reservation_time']))
                                print ('Existing Details: {}'.format(json_data['original_tee_time']['future_reservations'][0]['existing_details']))
                                captcha_loop = False
                        except:
                            print ('Failed Captcha Test, Retrying...')
    except:
        print ('No Times Available, Retrying...')
        time.sleep(1)

        




    


-- Keep a log of any SQL queries you execute as you solve the mystery.

command :
SELECT id, year, month, street, day, description FROM crime_scene_reports
WHERE year = 2024 AND day = 28 AND month = 7 AND street LIKE '%Humphrey%' ;

response:
case id: 295

The description says: duck stolen.

Answer: :

Theft of the CS50 duck took place at 10:15 am at the Humphrey Street bakery.
Interviews were conducted today with three witnesses who were present at the time –
each of their interview transcripts mentions the bakery.

       | summary |
time of theft: 10:15 a.m.
location: Humphrey Street bakery
number of witnesses interviewed on July 28, 2024: 3

commande :
SELECT name, transcript FROM interviews
WHERE month = 7 AND day = 28 AND transcript LIKE '%bakery%';

reponse :

ID     Name   year       Month             day

161    Ruth   2024        7                28

Sometime within ten minutes of the theft, I saw
the thief get into a car in the bakery parking lot and
drive away. If you have security footage from the
bakery parking lot, you might want to look for
cars that left the parking lot in that time frame.

162    Eugen  2024        7                28

I don't know the thief's name, but it was someone
I recognized. Earlier this morning, before I arriv
ed at Emma's bakery, I was walking by the ATM on L
eggett Street and saw the thief there withdrawing
some money.

163    Raymo  2024        7                28

As the thief was leaving the bakery, they called
someone who talked to them for less than a minute.
In the call, I heard the thief say that they were
planning to take the earliest flight out of Fiftyv
ille tomorrow. The thief then asked the person on
the other end of the phone to purchase the flight
ticket.


| summary |

3 reporters / witnesses: Ruth / Eugene / Raymond

Information:

Ruth:
Thief got into a car a few minutes after the theft
(seen on parking surveillance  check for cars leaving between 10:15 and 10:25 am)

Eugene:
Man he recognized, saw the thief earlier in the morning at the ATM on Leggett Street withdrawing cash.

Raymond:
Heard the call (duration < 1 min) between thief and accomplice.
Thief said they were planning to take the earliest flight departing Fiftyville the next day (July 29, 2024).
Thief then asked the person on the other end to buy the plane ticket (so → check bank account activity).

ATM = distributeur automatique.

    commande :
-Ruth’s statement : bakery_security_logs
For verification of the surveillance video and vehicles leaving the parking lot?

SELECT id, day, year, month, hour, minute, activity, license_plate
FROM bakery_security_logs
WHERE day = 28 AND year = 2024 AND month = 7 AND hour = 10;

response (information) (no other info):

  id   day    year   month   hour   minute              license_plate
| 260 | 28  | 2024 | 7     | 10   | 16     | exit     | 5P2BI95       |
| 261 | 28  | 2024 | 7     | 10   | 18     | exit     | 94KL13X       |
| 262 | 28  | 2024 | 7     | 10   | 18     | exit     | 6P58WS2       |
| 263 | 28  | 2024 | 7     | 10   | 19     | exit     | 4328GD8       |
| 264 | 28  | 2024 | 7     | 10   | 20     | exit     | G412CB7       |
| 265 | 28  | 2024 | 7     | 10   | 21     | exit     | L93JTIZ       |
| 266 | 28  | 2024 | 7     | 10   | 23     | exit     | 322W7JE       |
| 267 | 28  | 2024 | 7     | 10   | 23     | exit     | 0NTHK55       |


-Eugene’s statement
For verification of the surveillance (and vehicle leaving the parking lot)?
Hypothesis: maybe he paid for parking, so check if there is information in the bank statement about that.

SELECT id, year, month, day, atm_location, transaction_type FROM atm_transactions WHERE year = 2024 AND month = 7 AND day = 28 AND atm_location LIKE '%Leggett Street%';

response (information) (no other info):

+-----+------+-------+-----+----------------+------------------+
| id  | year | month | day |  atm_location  | transaction_type |
+-----+------+-------+-----+----------------+------------------+
| 246 | 2024 | 7     | 28  | Leggett Street | withdraw         |
| 264 | 2024 | 7     | 28  | Leggett Street | withdraw         |
| 266 | 2024 | 7     | 28  | Leggett Street | withdraw         |
| 267 | 2024 | 7     | 28  | Leggett Street | withdraw         |
| 269 | 2024 | 7     | 28  | Leggett Street | withdraw         |
| 288 | 2024 | 7     | 28  | Leggett Street | withdraw         |
| 313 | 2024 | 7     | 28  | Leggett Street | withdraw         |
| 336 | 2024 | 7     | 28  | Leggett Street | withdraw         |
+-----+------+-------+-----+----------------+------------------+

I still don't know if the “id” values are connected in any way, but we’ll see.

-Raymond’s statement
Find the Fiftyville airport:

SELECT id, abbreviation, full_name, city FROM airports;

+----+--------------+-----------------------------------------+---------------+
| id | abbreviation |                full_name                |     city      |
+----+--------------+-----------------------------------------+---------------+
| 1  | ORD          | O'Hare International Airport            | Chicago       |
| 2  | PEK          | Beijing Capital International Airport   | Beijing       |
| 3  | LAX          | Los Angeles International Airport       | Los Angeles   |
| 4  | LGA          | LaGuardia Airport                       | New York City |
| 5  | DFS          | Dallas/Fort Worth International Airport | Dallas        |
| 6  | BOS          | Logan International Airport             | Boston        |
| 7  | DXB          | Dubai International Airport             | Dubai         |
| 8  | CSF          | Fiftyville Regional Airport             | Fiftyville    |
| 9  | HND          | Tokyo International Airport             | Tokyo         |
| 10 | CDG          | Charles de Gaulle Airport               | Paris         |
| 11 | SFO          | San Francisco International Airport     | San Francisco |
| 12 | DEL          | Indira Gandhi International Airport     | Delhi         |
+----+--------------+-----------------------------------------+---------------+

-Search for all flights departing Fiftyville on July 29, 2024

SELECT flights.id, flights.origin_airport_id, flights.destination_airport_id, flights.year, flights.month, flights.day, flights.hour, flights.minute FROM flights
JOIN airports ON airports.id = flights.origin_airport_id
WHERE flights.year = 2024 AND flights.month = 7 AND flights.day = 29 AND airports.id = 8;

+----+-------------------+------------------------+------+-------+-----+------+--------+
| id | origin_airport_id | destination_airport_id | year | month | day | hour | minute |
+----+-------------------+------------------------+------+-------+-----+------+--------+
| 18 | 8                 | 6                      | 2024 | 7     | 29  | 16   | 0      |
| 23 | 8                 | 11                     | 2024 | 7     | 29  | 12   | 15     |
| 36 | 8                 | 4                      | 2024 | 7     | 29  | 8    | 20     |
| 43 | 8                 | 1                      | 2024 | 7     | 29  | 9    | 30     |
| 53 | 8                 | 9                      | 2024 | 7     | 29  | 15   | 20     |
+----+-------------------+------------------------+------+-------+-----+------+--------+

Know which airport corresponds to which ID:

| 6  | BOS          | Logan International Airport             | Boston        |

| 11 | SFO          | San Francisco International Airport     | San Francisco |

| 4  | LGA          | LaGuardia Airport                       | New York City |

| 1  | ORD          | O'Hare International Airport            | Chicago       |

| 9  | HND          | Tokyo International Airport             | Tokyo         |


-Search for phone_calls lasting less than one minute and taking place on 28 / 07 / 2024
Command :

SELECT id, caller, receiver, year, month, day, duration FROM phone_calls
WHERE duration < 60 AND year = 2024 AND day = 28 AND month = 7;

Response :

+-----+----------------+----------------+------+-------+-----+----------+
| id  |     caller     |    receiver    | year | month | day | duration |
+-----+----------------+----------------+------+-------+-----+----------+
| 221 | (130) 555-0289 | (996) 555-8899 | 2024 | 7     | 28  | 51       |
| 224 | (499) 555-9472 | (892) 555-8872 | 2024 | 7     | 28  | 36       |
| 233 | (367) 555-5533 | (375) 555-8161 | 2024 | 7     | 28  | 45       |
| 251 | (499) 555-9472 | (717) 555-1342 | 2024 | 7     | 28  | 50       |
| 254 | (286) 555-6063 | (676) 555-6554 | 2024 | 7     | 28  | 43       |
| 255 | (770) 555-1861 | (725) 555-3243 | 2024 | 7     | 28  | 49       |
| 261 | (031) 555-6622 | (910) 555-3251 | 2024 | 7     | 28  | 38       |
| 279 | (826) 555-1652 | (066) 555-9701 | 2024 | 7     | 28  | 55       |
| 281 | (338) 555-6650 | (704) 555-2131 | 2024 | 7     | 28  | 54       |
+-----+----------------+----------------+------+-------+-----+----------+

We look for someone who leaves the parking lot and has a matching license plate
Command :

SELECT id, name, phone_number, passport_number, license_plate FROM people
WHERE license_plate IN ('5P2BI95', '94KL13X', '6P58WS2', '4328GD8', 'G412CB7', 'L93JTIZ', '322W7JE', '0NTHK55');

+--------+---------+----------------+-----------------+---------------+
|   id   |  name   |  phone_number  | passport_number | license_plate |
+--------+---------+----------------+-----------------+---------------+
| 221103 | Vanessa | (725) 555-4692 | 2963008352      | 5P2BI95       |
| 243696 | Barry   | (301) 555-4174 | 7526138472      | 6P58WS2       |
| 396669 | Iman    | (829) 555-5269 | 7049073643      | L93JTIZ       |
| 398010 | Sofia   | (130) 555-0289 | 1695452385      | G412CB7       |
| 467400 | Luca    | (389) 555-5198 | 8496433585      | 4328GD8       |
| 514354 | Diana   | (770) 555-1861 | 3592750733      | 322W7JE       |
| 560886 | Kelsey  | (499) 555-9472 | 8294398571      | 0NTHK55       |
| 686048 | Bruce   | (367) 555-5533 | 5773159633      | 94KL13X       |
+--------+---------+----------------+-----------------+---------------+

We remove all those who are NOT in the list of callers

+--------+---------+----------------+-----------------+---------------+
|   id   |  name   |  phone_number  | passport_number | license_plate |
+--------+---------+----------------+-----------------+---------------+
| 398010 | Sofia   | (130) 555-0289 | 1695452385      | G412CB7       |
| 560886 | Kelsey  | (499) 555-9472 | 8294398571      | 0NTHK55       |
| 686048 | Bruce   | (367) 555-5533 | 5773159633      | 94KL13X       |
| 514354 | Diana   | (770) 555-1861 | 3592750733      | 322W7JE       |
+--------+---------+----------------+-----------------+---------------+

Search for passengers taking a flight departing Fiftyville on 29/07/2024 and see if it matches
Command :

SELECT people.id, people.name, people.phone_number, people.passport_number, people.license_plate FROM people
JOIN passengers ON passengers.passport_number = people.passport_number
WHERE people.passport_number IN ('1695452385', '8294398571', '5773159633', '3592750733');

+--------+--------+----------------+-----------------+---------------+
|   id   |  name  |  phone_number  | passport_number | license_plate |
+--------+--------+----------------+-----------------+---------------+
| 398010 | Sofia  | (130) 555-0289 | 1695452385      | G412CB7       |
| 514354 | Diana  | (770) 555-1861 | 3592750733      | 322W7JE       |
| 514354 | Diana  | (770) 555-1861 | 3592750733      | 322W7JE       |
| 514354 | Diana  | (770) 555-1861 | 3592750733      | 322W7JE       |
| 560886 | Kelsey | (499) 555-9472 | 8294398571      | 0NTHK55       |
| 686048 | Bruce  | (367) 555-5533 | 5773159633      | 94KL13X       |
+--------+--------+----------------+-----------------+---------------+

Search the passengers for flights departing Fiftyville that could correspond to these passengers
Command :

SELECT people.id, people.name, people.phone_number, people.license_plate, passengers.passport_number, flights.id, flights.origin_airport_id,
flights.destination_airport_id, flights.day, flights.month, flights.year FROM flights
JOIN passengers ON passengers.flight_id = flights.id
JOIN people ON people.passport_number = passengers.passport_number
WHERE passengers.passport_number IN ('1695452385', '8294398571', '5773159633', '3592750733') AND flights.day = 29 AND flights.month = 7 AND flights.year = 2024;


+--------+--------+----------------+---------------+-----------------+----+-------------------+------------------------+-----+-------+------+
|   id   |  name  |  phone_number  | license_plate | passport_number | id | origin_airport_id | destination_airport_id | day | month | year |
+--------+--------+----------------+---------------+-----------------+----+-------------------+------------------------+-----+-------+------+
| 514354 | Diana  | (770) 555-1861 | 322W7JE       | 3592750733      | 18 | 8                 | 6                      | 29  | 7     | 2024 |
| 398010 | Sofia  | (130) 555-0289 | G412CB7       | 1695452385      | 36 | 8                 | 4                      | 29  | 7     | 2024 |
| 686048 | Bruce  | (367) 555-5533 | 94KL13X       | 5773159633      | 36 | 8                 | 4                      | 29  | 7     | 2024 |
| 560886 | Kelsey | (499) 555-9472 | 0NTHK55       | 8294398571      | 36 | 8                 | 4                      | 29  | 7     | 2024 |
+--------+--------+----------------+---------------+-----------------+----+-------------------+------------------------+-----+-------+------+

Learn more about the transactions:
Command:

SELECT people.id, people.name, people.phone_number, people.passport_number, atm_transactions.id, atm_transactions.atm_location, atm_transactions.transaction_type FROM atm_transactions
JOIN bank_accounts ON bank_accounts.account_number = atm_transactions.account_number
JOIN people ON people.id = bank_accounts.person_id
WHERE year = 2024 AND month = 7 AND day = 28 AND atm_location LIKE '%Leggett Street%' AND people.passport_number IN ('3592750733', '1695452385', '5773159633', '8294398571');

+--------+-------+----------------+-----------------+-----+----------------+------------------+
|   id   | name  |  phone_number  | passport_number | id  |  atm_location  | transaction_type |
+--------+-------+----------------+-----------------+-----+----------------+------------------+
| 686048 | Bruce | (367) 555-5533 | 5773159633      | 267 | Leggett Street | withdraw         |
| 514354 | Diana | (770) 555-1861 | 3592750733      | 336 | Leggett Street | withdraw         |
+--------+-------+----------------+-----------------+-----+----------------+------------------+


To verify, we check if they called each other for less than 1 minute at the time of the theft

+-----+----------------+----------------+------+-------+-----+----------+
| id  |     caller     |    receiver    | year | month | day | duration |
+-----+----------------+----------------+------+-------+-----+----------+
| 221 | (130) 555-0289 | (996) 555-8899 | 2024 | 7     | 28  | 51       |
| 224 | (499) 555-9472 | (892) 555-8872 | 2024 | 7     | 28  | 36       |
| 233 | (367) 555-5533 | (375) 555-8161 | 2024 | 7     | 28  | 45       |
| 251 | (499) 555-9472 | (717) 555-1342 | 2024 | 7     | 28  | 50       |
| 254 | (286) 555-6063 | (676) 555-6554 | 2024 | 7     | 28  | 43       |
| 255 | (770) 555-1861 | (725) 555-3243 | 2024 | 7     | 28  | 49       |
| 261 | (031) 555-6622 | (910) 555-3251 | 2024 | 7     | 28  | 38       |
| 279 | (826) 555-1652 | (066) 555-9701 | 2024 | 7     | 28  | 55       |
| 281 | (338) 555-6650 | (704) 555-2131 | 2024 | 7     | 28  | 54       |
+-----+----------------+----------------+------+-------+-----+----------+

Réponse :

| 233 | (367) 555-5533 | (375) 555-8161 | 2024 | 7     | 28  | 45       |

So we have proof that the thieves are Bruce and Diana (Bruce = thief, Diana = accomplice), because they called each other for 45 seconds (less than one minute as indicated)

I will now display all the information about them that confirms and clearly shows that the two are the thieves

SELECT people.id, people.name, people.phone_number, people.passport_number, people.license_plate FROM people
WHERE people.passport_number in ('5773159633', '3592750733');

+--------+-------+----------------+-----------------+---------------+
|   id   | name  |  phone_number  | passport_number | license_plate |
+--------+-------+----------------+-----------------+---------------+
| 514354 | Diana | (770) 555-1861 | 3592750733      | 322W7JE       |
| 686048 | Bruce | (367) 555-5533 | 5773159633      | 94KL13X       |
+--------+-------+----------------+-----------------+---------------+

And we will make everything match together using a single command.

The constraints here:

-Withdrew money on Leggett Street the same morning (28/07/2024)
-Made a phone call < 1 minute at the time of the theft (28/07/2024)
-Took a flight on 29/07 departing from Fiftyville
-The vehicles present in the parking lot between 10:15 and 10:25

Command :

SELECT people.id, people.name, people.phone_number, people.passport_number, people.license_plate, flights.destination_airport_id  FROM people
JOIN bank_accounts ON bank_accounts.person_id = people.id
JOIN atm_transactions ON atm_transactions.account_number = bank_accounts.account_number
JOIN phone_calls AS calls_out ON calls_out.caller = people.phone_number
JOIN phone_calls AS calls_in  ON calls_in.receiver = people.phone_number
JOIN passengers ON passengers.passport_number = people.passport_number
JOIN flights ON flights.id = passengers.flight_id
JOIN airports AS origin_airport ON origin_airport.id = flights.origin_airport_id
JOIN airports AS destination_airport ON destination_airport.id = flights.destination_airport_id
WHERE atm_transactions.atm_location LIKE '%Leggett%'
AND atm_transactions.day = 28
AND atm_transactions.month = 7
AND atm_transactions.year = 2024
AND calls_out.duration < 60
AND calls_out.caller = '(367) 555-5533'
AND flights.origin_airport_id = 8
AND flights.day = 29
AND flights.month = 7
AND flights.year = 2024
AND people.license_plate IN ('5P2BI95','94KL13X','6P58WS2','4328GD8','G412CB7','L93JTIZ','322W7JE','0NTHK55');


Voila

+----+--------------+-----------------------------------------+---------------+
| id | abbreviation |                full_name                |     city      |
+----+--------------+-----------------------------------------+---------------+
| 4  | LGA          | LaGuardia Airport                       | New York City |


The THIEF is: Bruce
The city the thief ESCAPED TO: 4 = New York City
The ACCOMPLICE is: Diana

After the check50 error, I re-checked my reasoning.
The accomplice was incorrect.
Robin is the accomplice.
Why?

My mistake was assuming that the person the thief called was accomplice without explicitly verifying it.
I initially inferred the accomplice from a short phone call instead of identifying the exact receiver of the thief’s call.
After re-checking the phone_calls table and linking the receiver to the flight booking,
I confirmed that the accomplice is Robin.

So :

The THIEF is: Bruce
The city the thief ESCAPED TO: 4 = New York
The ACCOMPLICE is: Robin

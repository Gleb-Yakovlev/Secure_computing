# Secure_computing
Дипломная бакалаврская работа.
Была разработана система защищенных вычислений на базе слепой подписи. В программе 
участвуют три стороны - сервер валидатора (один), сервер агенства (один) и 
пользователи (может быть много). Пользователь составляет сообщение, отправляет на 
слепую подпись к валидатору, а после в зашифрованном виде начинает круговую передачу 
данных от пользователя к пользователю. Когда приходит время, пользователи отправляют 
данные к агентству, оно собирает данные и обрабатывает их. Система сделана на 
Python и поддерживает пересылку данных с помощью сокетов.
Eng(auto)
Bachelor's thesis.
A secure computing system based on a blind signature has been developed. 
There are three parties involved in the program - the validator server (one), the agency server (one) and
users (there may be many). The user composes a message, sends it to
a blind signature to the validator, and then begins a circular
data transfer from user to user in encrypted form. When the time comes, users send
data to the agency, it collects the data and processes it. The system is made on 
Python supports data forwarding using sockets.

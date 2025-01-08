Во четвртата домашна работа, треба да го рефакторирате кодот од третата домашна работа,
да ги префрлите дел од функционалностите на апликациjата во АПИ/микросервиси и да
jа подготвите апликациjата и микросервисите за работа во контеjнер. На краj, треба да jа
инсталирате апликациjата и сервисите во облак.


 Рефакторирање на кодот
 
Рефакторираjте го кодот на вашата апликациjата да следи наjмалку еден од софтверските шаблони дискутирани на предавањата. Посавете документ со обjаснување коj шаблон
сте го имплементирале и зошто. Рефакторираниот код треба да:
• Биде jасен: Кодот треба да биде лесен за читање и разбирање.
• Биде доследен: Користеѕе ист стил на именување за променливи и методи низ целиот
код.
• Има добри имиња: Променливите и методите треба да имаат jасни и значаjни имиња.
• Биде добро документиран: Имињата треба да го обjаснуваат кодот. Ако не е така,
додадете кратки коментари за да разjасните што прави кодот или да обjасните неjасни
имиња на методи или параметри.
• Биде лесен за одржување: Кодот треба да биде едноставен за ажурирање или подобрување во иднина.
• Биде повторно употреблив: Напишете код што може да се користи на други места
во апликациjата.
• Избегнува повторување: Отстранете дупликатен код правеj´ки jа апликациjата го
пофлексибилна и модуларна.
• Биде ефикасен: Користете алгоритми кои се едноставни и брзи, избегнуваj´ки непотребна сложеност.


 АПИ/Микросервиси

Преработете некои функции од вашата апликациjа како микросервиси кои комуницираат преку АПИ. Микросервисите се мали, независни делови од апликациjата кои
можат да работат самостоjно. Земете неколку функции од вашата апликациjа, изградете ги
како посебни програми и осигураjте се дека можат да функционираат самостоjно. Секоj
микросервис треба да биде создаден како своj проект. Потоа, овозможете комуникациjа поме´гу микросервисите и главната апликациjа користеj´ки АПИ.
Можете да ги следите овие туториjали за примери како да го направите ова користеj´ки
Spring. Ако користите друга технологиjа, можете да ги прилагодите чекорите:
• https://spring.io/blog/2015/07/14/microservices-with-spring
• https://www.javatpoint.com/microservices
• https://developer.okta.com/blog/2019/05/22/java-microservices-spring-boot-spring-cloud


 Контеjнеризациjа и инсталациjа во облак
 
Подгответе jа вашата апликациjа за деплоjирање преку контеjнеризациjа и деплоjирање во облак. Контеjнерите се самостоjни единици кои jа вклучуваат вашата апликациjа и сите неjзини зависности, обезбедуваj´ки конзистентност во различни опкружувања.
Користете алатка како што е Docker за пакување на вашата апликациjа во контеjнер.
За пове´ке информации за користење Docker, погледнете:
• https://docs.docker.com/get-started/
Дополнително, следниот водич обезбедува пример како да се контеjнеризира микросервис со
Docker:
• https://azure.microsoft.com/en-us/free/students/
• https://aws.amazon.com/education/awseducate/
Имаjте на ум дека ´ке мора да почекате неколку денови за потврдата на вашиот статус на
студент, коjа е потребна за да ги користите сервисите.
Кодот за четвртата домашна поставете го на GitHub во папка именувана Домашна 4.
Важно: Осигурете се дека верзиjата на апликациjата за третата домашна работа останува
непроменета. За да го направите ова, избегнуваjте да работите на гранката поврзана со платформата каде што е деплоjирана апликациjата, или исклучете ги автоматските деплоjменти.
Обjавете jа обновената апликациjа за четвртата домашна работа на нов линк и вклучете го
овоj линк во About секциjата на вашиот GitHub репозиториум.
Рокот за изработка на третата домашна работа е до 19 jануари 2025. Имаjте во предвид
дека овоj рок е конечен и нема да биде продолжен.
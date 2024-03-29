# k_2_82
Программа для проверки систем радиосвязи с помощью установки для измерения параметров К2-82. Используется для проведения планового технического обслуживания носимых радиостанций на предприятиях ОАО РЖД

---

## Описание

Программа имеет графический интерфейс и работает под управлением OS Windows. Для начала работы необходимо перевести прибор К2-82 в состояние УСТ и ДУ 
(должны загораться соответствующие индикаторы). Радиостанцию необходимо подключить к источнику питания и к технологической приставке (программатору) для связи с ПК 
через аксессуарный разъем. Для связи с К2-82 необходимо подключить ВЧ адаптер к антенному разъему радтиостанции. Для запуска цикла проверки и получения характеристик радиостанции нажать кнопку "Старт проверки" в программе и следовать дальнейшим инструкциям. Связь с радиостанцией и К2-82 осуществляется чере COM порты

#### Назначения и настройки COM портов:

1. COM1 (Порт можно изменить в настройках) соединяется с технологической приставкой для установки связи с носимой радиостанцией. 
При завершении цикла проверки считывает серийный номер.

2. COM2 (Порт можно изменить в настройках) соединяется с приставкой для измерения параметров радиостанции к2-82 и посылает алгоритм сигналов для 
проведения технического обслуживания. Проверка делится на несколько этапов, после завершения каждого этапа считываются показатели с прибора к2-82

Выбрать нужный COM порт можно в верхнем меню в разделе настройки. При перезапуске программы выбранные COM порты сохраняются

### Этапы проверки радиостанции:

Перед началом проверки на К2-82 посылается сигнал определяющий состояние прибора и доступа к радиостанции, 
программа переключается на проверку несущей частоты и в зависимости от результата определяет включен ли прибор и находится ли радиостанци в режиме передачи.

1. Проверка несущей частоты
2. Проверка мощности передатчика
3. Проверка чувствительности модуляционного входа
4. Проверка коэффициента нелинейных искожений передатчика
5. Проверка максимальной девиации передатчика
6. Проверка отклонения частоты от номинала
7. Проверка мощности приемника
8. Проверка коэффициента нелинейных искажений приемника
9. Проверка порога срабатывания шумоподавителя
10. Считывание серийного номера

### Завершение цикла проверки

После завершения цикла проверки носимой радиостанции все полученные характеристики заносятся в электронную ведомость (главная таблица программы), 
установка К2-82 возвращается в исходное состояние и готова для дальнейшей работы с программой.

---

## Используемые технологии:

Python 3, Pyseryal, PyQt 5, unittest , xlwt

## Установка зависимостей

     pip install requirements.txt
     
## Запуск программы

     python main.py
     
## Сборка программы в exe файл

     python setup.py build

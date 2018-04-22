# Tianchi2017IMQP-TeamExcited

TeamExcited of Tianchi Industrial AI Competition 2017: Intelligent Manufacturing and Quality Prediction

*cooperated with [@npuzj](<https://github.com/npuzj>) and [pr0grammer(@hard-working)](<https://github.com/hard-working>)*

## `\raw_data\`

Converting the raw data of training and test to pickled binary files.

* `raw_data.bin.7z`: raw training data pickled into binary file
* `raw_test_data.bin.7z`: raw test data pickled into binary file
* `xlsx2bin.py`: convertor, run this when folder contains the xlsx file

## Training Data Form

* A (ID)
* B (str)
* C ~ HX, 210 X (1 ~ 231)
* HY (str)
* HZ ~ ABX, 220 X (1 ~ 571)
* ABY (str)
* ABZ ~ ACT, 300 X (1 ~ 21)
* ACU (str)
* ACV ~ AJI, 310 X (1 ~ 207)
* AJJ (str, len(str) == 2)
* AJK ~ ARW, 311 X (1 ~ 225)
* ARX ~ BML, 261 X (226 ~ 763)
* BMM (int)
* BMN ~ CMP, 312 X (1 ~ 798)
* CMQ (str)
* CMR ~ ELB, 330 X (1 ~ 1311)
* ELC (int)
* ELD ~ EST, 340 X (1 ~ 199)
* ESU (str)
* ESV ~ FDI, 344 X (1 ~ 110)
* FDJ (str)
* FDK ~ HHF, 360 X (1 ~ 1452)
* HHG ~ HOG, 400 X (1 ~ 230)
* HOH ~ HUX, 420 X (1 ~ 230)
* HUY (str, len(str) == 3)
* HUZ ~ IDD, 440 AX (1 ~ 213)
* IDE (int)
* IDF ~ IRW, 520 X (1 ~ 434)
* IRX (str)
* IRY ~ KVT, 750 X (1 ~ 1452)
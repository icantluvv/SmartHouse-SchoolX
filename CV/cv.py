# started work
import cv2
# на 4 строке создаю переменную, указываю местоположение обученного интелекта в библиотеке open cv
face_cascade_db = cv2.CascadeClassifier(cv2.data.haarcascades+'haarcascade_frontalface_default.xml') 

#пробую распознать лицо на картинке
img = cv2.imread(r"C:\Users\User\Documents\GitHub\SmartHouse-SchoolX\CV\WIN_20230225_16_17_22_Pro.jpg")
#преобразую картинку в оттенки серого
img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

faces = face_cascade_db.detectMultiScale(img_gray, 1.1, 19)

#вывожу результат на экран
cv2.imshow('rez',img_gray)

#добавляю задержку
cv2.waitKey()

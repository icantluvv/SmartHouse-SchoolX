# started work
import cv2
# на 4 строке создаю переменную, указываю местоположение обученного интелекта в библиотеке open cv
face_cascade_db = cv2.CascadeClassifier(cv2.data.haarcascades+'haarcascade_frontalface_default.xml') 

#обращаюсь к видеокамере, чтобы получить картинку с нее
cap = cv2.VideoCapture(0)

#цикл для постоянного считывания картинки. Результат выполнения будет записан в переменную success, в img записывается картинка, которая считывается с экрана
while True:
    success, img = cap.read()

    #пробую распознать лицо на картинке
    #img = cv2.imread(r"C:\Users\User\Documents\GitHub\SmartHouse-SchoolX\CV\WIN_20230225_16_17_22_Pro.jpg")
    #преобразую картинку в оттенки серого
    img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    #в переменную закладываю список найденных координат наших лиц на картинке
    faces = face_cascade_db.detectMultiScale(img_gray, 1.1, 19)
    #обращаюсь к найденным координатам лиц и вывожу зеленый прямоугольник вокруг них
    for (x,y,w,h) in faces:
        cv2.rectangle(img, (x,y), (x+w, y+h),(0,255,0), 2)

    #вывожу результат на экран
    cv2.imshow('rez',img)

    #добавляю задержку
    if cv2.waitKey(1) & 0xff == ord('q'):
        break

#освобождаю камеру
cap.release()
cv2.destroyAllWindows()

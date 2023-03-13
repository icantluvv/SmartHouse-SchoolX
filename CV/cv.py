import face_recognition
import imutils
import pickle
import time
import cv2
import os
 
##найти путь к xml-файлу, содержащему файл Каскады Харда
cascPathface = os.path.dirname(
 cv2.__file__) + "/data/haarcascade_frontalface_alt2.xml"
# загрузите harcaascade в класс
faceCascade = cv2.CascadeClassifier(cascPathface)
# загрузите данных
data = pickle.loads(open('face_enc', "rb").read())
 
print("Streaming started")
video_capture = cv2.VideoCapture(0)
# loop over frames from the video file stream
while True:
    #захват кадра
    ret, frame = video_capture.read()
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = faceCascade.detectMultiScale(gray,
                                         scaleFactor=1.1,
                                         minNeighbors=5,
                                         minSize=(60, 60),
                                         flags=cv2.CASCADE_SCALE_IMAGE)
 
    # преобразуйте входной кадр из BGR в RGB 
    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    # теперь личико запихиваем во входные данные
    encodings = face_recognition.face_encodings(rgb)
    names = []
    # обведите петлей лицевые вставки, надрежьте
    # у нас есть несколько встраиваний для нескольких fcaes
    for encoding in encodings:
        #Сравните кодировки с кодировками в данных["кодировки  то что мы и длелаи вов тором файле"]
        #Совпадения содержат массив с логическими значениями и True для вложений, которым он точно соответствует
        #и False для остальных
        matches = face_recognition.compare_faces(data["encodings"],
         encoding)
        #установите name =inknown, если кодировка не совпадает
        name = "Unknown"
        # проверьте, нашли ли мы совпадение
        if True in matches:
            #Находим позиции, в которых мы получаем True, и сохраняем их
            matchedIdxs = [i for (i, b) in enumerate(matches) if b]
            counts = {}
            #перебирайте сопоставленные индексы и поддерживайте подсчет для
            # каждое распознанное лицо - лицо
            for i in matchedIdxs:
                #Check the names at respective indexes we stored in matchedIdxs
                name = data["names"][i]
                #increase count for the name we got
                counts[name] = counts.get(name, 0) + 1
            #set name which has highest count
            name = max(counts, key=counts.get)
 
 
        #обновите список имен
        names.append(name)
        # loop over the recognized faces
        for ((x, y, w, h), name) in zip(faces, names):
            # rescale the face coordinates
            # draw the predicted face name on the image
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
            cv2.putText(frame, name, (x, y), cv2.FONT_HERSHEY_SIMPLEX,
             0.75, (0, 255, 0), 2)
    cv2.imshow("Frame", frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
video_capture.release()
cv2.destroyAllWindows()
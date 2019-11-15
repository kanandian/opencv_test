import cv2
cap=cv2.VideoCapture(0)
i=1
while(i<=100):
    ret ,frame = cap.read()
    k=cv2.waitKey(1)
    # if k==27:
    #     break
    # elif k==ord('s'):
    cv2.imwrite('images-cv/'+str(i)+'.jpg',frame)
    i+=1
    cv2.imshow("capture", frame)
cap.release()
cv2.destroyAllWindows()

#     k = cv2.waitKey(1)
#     if k == 27:
#         break
#     elif k == ord('s'):
#         cv2.imwrite('images-cv/' + str(i) + '.jpg', frame)
#         i += 1
#     cv2.imshow("capture", frame)
# cap.release()
# cv2.destroyAllWindows()
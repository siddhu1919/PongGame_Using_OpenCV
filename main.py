import cv2
import cvzone
from cvzone.HandTrackingModule import HandDetector
import numpy as np

import pygame  # Import pygame

cap = cv2.VideoCapture(1)
cap.set(3, 1280)
cap.set(4, 720)

# Importing all images
imgBackground = cv2.imread("Resources/bg.jpg")
imgGameOver = cv2.imread("Resources/gameOver.png")
imgBall = cv2.imread("Resources/Ball.png", cv2.IMREAD_UNCHANGED)
imgBat1 = cv2.imread("Resources/bat1.png", cv2.IMREAD_UNCHANGED)
imgBat2 = cv2.imread("Resources/bat2.png", cv2.IMREAD_UNCHANGED)


# Hand Detector
detector = HandDetector(detectionCon=0.8, maxHands=2)

# Variables
ballPos = [100, 100]
speedX = 15
speedY = 15
gameOver = False
score = [0, 0]

# Code For FullScreen Sized Window
# Set the window to be resizable, then make it fullscreen
cv2.namedWindow("Image", cv2.WINDOW_NORMAL)
cv2.setWindowProperty("Image", cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)


while True:
    _, img = cap.read()
    img = cv2.flip(img, 1)
    imgRaw = img.copy()

    # Find the hand and its landmarks
    hands, img = detector.findHands(img, flipType=False)  # with draw

    # Overlaying the background image
    img = cv2.addWeighted(img, 0.2, imgBackground, 0.8, 0)

    # Check for hands
    if hands:
        for hand in hands:
            x, y, w, h = hand["bbox"]
            h1, w1, _ = imgBat1.shape
            y1 = y - h1 // 2
            y1 = np.clip(y1, 20, 415)

            if hand["type"] == "Left":
                img = cvzone.overlayPNG(img, imgBat1, (59, y1))
                if 59 < ballPos[0] < 59 + w1 and y1 < ballPos[1] < y1 + h1:
                    speedX = -speedX
                    ballPos[0] += 30
                    score[0] += 1

            if hand["type"] == "Right":
                img = cvzone.overlayPNG(img, imgBat2, (1195, y1))
                if 1195 - 50 < ballPos[0] < 1195 and y1 < ballPos[1] < y1 + h1:
                    speedX = -speedX
                    ballPos[0] -= 30
                    score[1] += 1

    # Game Over
    if ballPos[0] < 40 or ballPos[0] > 1200:
        gameOver = True

    if gameOver:
        img = imgGameOver
        cv2.putText(
            img,
            str(score[1] + score[0]).zfill(2),
            (585, 360),
            cv2.FONT_HERSHEY_COMPLEX,
            2.5,
            (200, 0, 200),
            5,
        )

    # If game not over move the ball
    else:

        # Move the Ball
        if ballPos[1] >= 500 or ballPos[1] <= 10:
            speedY = -speedY

        ballPos[0] += speedX
        ballPos[1] += speedY

        # Draw the ball
        img = cvzone.overlayPNG(img, imgBall, ballPos)

        cv2.putText(
            img,
            str(score[0]),
            (300, 650),
            cv2.FONT_HERSHEY_COMPLEX,
            3,
            (255, 255, 255),
            5,
        )
        cv2.putText(
            img,
            str(score[1]),
            (900, 650),
            cv2.FONT_HERSHEY_COMPLEX,
            3,
            (255, 255, 255),
            5,
        )

    img[580:700, 20:233] = cv2.resize(imgRaw, (213, 120))

    cv2.imshow("Image", img)
    key = cv2.waitKey(1)
    if key == ord("r"):
        ballPos = [100, 100]
        speedX = 15
        speedY = 15
        gameOver = False
        score = [0, 0]
        imgGameOver = cv2.imread("Resources/gameOver.png")
    elif key == 32:  # ASCII value of spacebar
        break  # Exit the loop, effectively closing the app


# Pygame "Thank You for Playing" message
pygame.init()
# Load an image to use as the icon
icon = pygame.image.load('Resources\pikachu.png')  # Update the path to your icon file

# Set the window icon
pygame.display.set_icon(icon)



screen = pygame.display.set_mode((600, 400)) # Default ((500, 300))
pygame.display.set_caption("Made with ❤️ by SID.")
font = pygame.font.Font(None, 36)
text = font.render("Thank You for Playing!", True, (255, 255, 255))
text_rect = text.get_rect(center=(300, 200))

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    screen.fill((0, 0, 0))
    screen.blit(text, text_rect)
    pygame.display.flip()
    pygame.time.wait(3000)  # Display the message for 3 seconds
    running = False

pygame.quit()



# Release the video capture object and close OpenCV windows
cap.release()
cv2.destroyAllWindows()
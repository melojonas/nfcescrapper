import cv2
import os.path

def read_qr_code(filename = ""):
    """Read an image and read the QR code.
    
    Args:
        filename (string): Path to file
    
    Returns:
        qr (string): Value from QR code
    """
    
    if os.path.isfile(filename) and (filename != ""):
        img = cv2.imread(filename)
        detector = cv2.QRCodeDetector()
        data, bbox, _ = detector.detectAndDecode(img)
        if data:
            return data
        else:
            print("QR code não detectado.")
            exit()

def scan_qr_code():
    """Read an image and read the QR code.
    None -> string"""
    
    cap = cv2.VideoCapture(0)
    detector = cv2.QRCodeDetector()
    url = ""

    while True:
        _, img = cap.read()
        # detect and decode
        data, bbox, _ = detector.detectAndDecode(img)
        # check if there is a QRCode in the image
        if data:
            url = data
            break

        if cv2.waitKey(1) == ord("q"):
            break
    
    cap.release()
    cv2.destroyAllWindows()

    if url == "":
        print("QR code não detectado")
        exit()
    else:
        print("QR code detectado")
        print("URL: ", url)
    
    return url
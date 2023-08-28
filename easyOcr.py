import easyocr


reader = easyocr.Reader(['en'])



def characterDetection(image)-> str:
    return reader.readtext(image)




if __name__ == '__main__':

    import PIL
    im = PIL.Image.open("/images/modelPlate.jpeg")

    print(characterDetection(im))




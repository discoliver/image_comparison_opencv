import time
import csv
import os
import sys
import cv2
from skimage.measure import compare_ssim

#Remove the old result file if exists, otherwise will let user know there is no result file in current folder
def remove_old_result():
    if os.path.exists('result.csv'):
        os.remove('result.csv')
    else:
        print("This is the first time you running this tool or you have deleted the previous result file")
        return;

#Read the input csv file with error handdling
def read_input_file():
    try:
        with open(sys.argv[1], 'r') as f:
            reader = csv.reader(f)
            next(reader)
            image_list = list(reader)
            return image_list
    except IndexError:
        print ('Opps You forget to add a cvs file, try python compare.py filename.cvs ....')
        raise

#Write the headline of the result file
def write_headline(c1, c2, c3, c4):
    with open('result.csv', 'w') as csvFile:
        writer = csv.writer(csvFile)
        writer.writerow([c1, c2, c3, c4])

#Write a row of compare result into result.cvs
def write_output(image_row):
    with open('result.csv', 'a') as csvFile:
        writer = csv.writer(csvFile)
        writer.writerow(image_row)
    csvFile.close()

#Operate extraction and comparison on each row of input image pairs.
def loop_thru_image_list(image_list):
    for image_row in image_list:

        #Timer for calculating elapsed_time
        start_time = time.time()

        #Extract the image pair
        imageA = cv2.imread(image_row[0])
        imageB = cv2.imread(image_row[1])

        #convert between RGB and grayscale
        gray_imageA = cv2.cvtColor(imageA, cv2.COLOR_BGR2GRAY)
        gray_imageB = cv2.cvtColor(imageB, cv2.COLOR_BGR2GRAY)

        #Compute the mean structural similarity index between two images.
        ssim_score = compare_ssim(gray_imageA, gray_imageB)

        #converting from range [-1, 1] to [0, 1]
        score = ssim_score * 0.5 + 0.5

        #In Bjorn case, expecting 0 for identical image, which is the reverse of ssim
        similarity = 1 - score

        #Debug code and testing
        #print("SSIM: {}".format(similarity))
        #cv2.imshow("Grey image demo", gray_imageA)
        #cv2.waitKey(0)
        #cv2.destroyAllWindows()
        #print (gray_imageA)
        #print (gray_imageB)

        elapsed_time = time.time() - start_time

        image_row.insert(2, similarity)
        image_row.insert(3, elapsed_time)

        write_output(image_row)

def main():
    remove_old_result()

    image_list = read_input_file()

    write_headline("image1", "image2", "similar", "elapsed")

    loop_thru_image_list(image_list)

    #Debug: Qucik output for preview
    # with open("result.csv") as f:
    #     reader = csv.reader(f)
    #     for row in reader:
    #         print(" ".join(row))

if __name__ == "__main__":
    main()
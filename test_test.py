import sys
import cv2 as cv
import numpy as np
import pytesseract
from PIL import Image, ImageFont, ImageDraw
from decimal import Decimal, ROUND_UP


listd = None
col = 4
colP = 2
a = b = c = None
global xnew1, xnew2, xnew3, ynew1, ynew2, ynew3


def main(argv):

    ## [load]
    default_file = 'or12.png'
    filename = argv[0] if len(argv) > 0 else default_file

    # Loads an image
    src = cv.imread(cv.samples.findFile(filename), cv.IMREAD_COLOR)

    # Check if image is loaded fine
    if src is None:
        print ('Error opening image!')
        print ('Usage: hough_lines.py [image_name -- default ' + default_file + '] \n')
        return -1

    gray_image = cv.cvtColor(src, cv.COLOR_BGR2GRAY)
 
    #edited
    dst = cv.Canny(src, 20, 200, None, 3)
   
    # Copy edges to the images that will display the results in BGR
    cdst = cv.cvtColor(dst, cv.COLOR_GRAY2BGR)
    cdstP = np.copy(cdst)
    gray_image1 = cv.cvtColor(cdstP, cv.COLOR_BGR2GRAY)


        # Probabilistic Line Transform
    linesP = cv.HoughLinesP(dst, 1, np.pi / 180, 80, None, 20, 10) 

    def storeLineCoordinate() :
        
        #result_array2 = np.array([])
        global listd, gradientlist, values, keys, v_x, v_y, m_xy
        #listd is the list of coordinates
        listd = [[0] * col for i in range(0,len(linesP))]
        #list of gradients
        gradientlist = []
        for i in range(0, len(linesP)):
            l = linesP[i][0]
            cv.line(cdstP, (l[0], l[1]), (l[2], l[3]), (0, 255, 0), 1)
            listd[i][0] = l[0]
            listd[i][1] = l[1]
            listd[i][2] = l[2]
            listd[i][3] = l[3]

            #get the gradient of all the possible lines coming from probabilistic hough line transformation
            #to identify the parrellel lines to remove duplicate lines
            for k in range(1,len(linesP)):
                    #listd[i][0][i][1][i][2][i][3] -> x1,y1,x2,y2
                    #y diff   
                    v_y = listd[i][3] - listd[i][1]
                    #x diff
                    v_x = listd[i][2] - listd[i][0]
                    
                
            for t in range(0,i+1):
                    #if the x diff is greater than zero, can calculate gradient
                    if v_x != 0 and v_y !=0 : 
                        #gradient
                        m_xyt = v_y / v_x
                        m_xy = round(m_xyt,1)

                    #if the x diff is zero, gradient is infinite. then assign a value to that. vertical line  
                    if v_x == 0:
                        m_xy = "a"

                    if v_y == 0:
                        m_xy = "b"
            gradientlist.insert(t, m_xy)
                
            print("m_xy",m_xy)
            print("v_y",v_y)
            print("v_x",v_x)


         
        print (gradientlist)
        print(listd)

   
        #create a dictionary to get the corresponding coordinates
        #of lines for gradients without getting duplicates
        d = {} #Dictionary
        #store gradients and corresponding line coordinates in a dictionary
        for index in range(min(len(listd),len(listd))):
            
            # for index number in the length of smallest list
            d[gradientlist[index]] = listd[index]
            # add the value of gradientlist at that place to the dictionary with value of listd
        print ("dictionary:",d)

        # split dictionary into keys and values 
        keys = [] 
        values = [] 
        
        items = d.items()
    
        for item in items: 
            keys.append(item[0]), values.append(item[1]) 
        
        # printing keys and values separately 
        print ("keys : ", str(keys)) 
        print ("values : ", str(values))

        ####do do do do???????????
        # if len(keys) > 3:
        #     print('tttttt')
            
        #     for p in range(0,len(keys)):
        #         for q in range(p+1,len(keys)):
        #             print('lllllllllllllll')
        #             if (keys[p] - keys[q]) <= 0.1 or (keys[p] - keys[q]) >= -0.1 :
        #                 key =  keys[p]
        #         print(key)
                        



   
    num1 = num2 = num3 = 0
    def generateLineEquation() :
        
        #get the x and y cordinates of the intersection points of line pairs 
        x1 = ((values[1][1]-(((values[1][3] - values[1][1]) / (values[1][2] - values[1][0])) *values[1][0])) - (values[0][1]-(((values[0][3] - values[0][1])/(values[0][2] - values[0][0]))*values[0][0])))/(((values[0][3] - values[0][1])/(values[0][2] - values[0][0]))-((values[1][3] - values[1][1])/(values[1][2] - values[1][0])))
        xnew1 = int(x1)
        y1 =((((values[1][3] - values[1][1])/(values[1][2] - values[1][0])) * x1) + (values[1][1]-(((values[1][3] - values[1][1])/(values[1][2] - values[1][0])))*values[1][0]))
        ynew1 = int(y1)
        print("xnew1=",xnew1) 
        print("ynew1=",ynew1)

        x2 = ((values[2][1]-(((values[2][3] - values[2][1]) / (values[2][2] - values[2][0])) *values[2][0])) - (values[0][1]-(((values[0][3] - values[0][1])/(values[0][2] - values[0][0]))*values[0][0])))/(((values[0][3] - values[0][1])/(values[0][2] - values[0][0]))-((values[2][3] - values[2][1])/(values[2][2] - values[2][0])))
        xnew2 = int(x2)
        y2 =((((values[2][3] - values[2][1])/(values[2][2] - values[2][0])) * x2) + ((values[2][1]-(((values[2][3] - values[2][1])/(values[2][2] - values[2][0])))*values[2][0])))
        ynew2 = int(y2)
        print("xnew2=",xnew2) 
        print("ynew2=",ynew2)

        x3 = ((values[2][1]-(((values[2][3] - values[2][1]) / (values[2][2] - values[2][0])) *values[2][0])) - (values[1][1]-(((values[1][3] - values[1][1])/(values[1][2] - values[1][0]))*values[1][0])))/(((values[1][3] - values[1][1])/(values[1][2] - values[1][0]))-((values[2][3] - values[2][1])/(values[2][2] - values[2][0])))
        xnew3 = int(x3)
        y3 =((((values[2][3] - values[2][1])/(values[2][2] - values[2][0])) * x3) + ((values[2][1]-(((values[2][3] - values[2][1])/(values[2][2] - values[2][0])))*values[2][0])))
        ynew3 = int(y3)
        print("xnew3=",xnew3) 
        print("ynew3=",ynew3)


        #puth the intersection coordinates to a list called arr
        arr = [[xnew1,ynew1],[xnew2,ynew2],[xnew3,ynew3]]
        #cv.line(cdstP, (arr[0], arr[1]), (arr[2], arr[3]), (255,128,0), 2, cv.LINE_AA)
        print(arr)
        print("*************************")
        print(" ")

        #based on the identified intersection points, draw the 3 lines of the triangle in 3 different colors 
        #color in BGR
        #yellow line
        cv.line(cdstP,(xnew1,ynew1),(xnew2,ynew2),(0,255,255),2)
        #blue line
        cv.line(cdstP,(xnew1,ynew1),(xnew3,ynew3),(255,18,1),2)
        #pink line
        cv.line(cdstP,(xnew2,ynew2),(xnew3,ynew3),(114,128,250),2)



        a = 10
        b = 20
        c = 30
        for i in range(0,3):
            #finding the y diif and x diff of each line and get the gradient of each line
            xdiff = values[i][2] - values[i][0]
            ydiff = values[i][3] - values[i][1]
            s = ydiff/xdiff
            
            m = Decimal(s).quantize(Decimal(".1"), rounding=ROUND_UP)
            print(xdiff)
            print(ydiff) 
            if xdiff != 0 and ydiff != 0:
                t = values[i][1]-(m*values[i][0])
                c = Decimal(t).quantize(Decimal(".1"), rounding=ROUND_UP)
                print("c="+str(c))
            
            #y = m*x
                
                if ydiff==0:
                    print("y="+ values[i][3])
                elif xdiff==0:
                    print("y="+ values[i][0])
                elif xdiff != 0 and ydiff != 0:
                    if c == 0:
                        print("y="+ str(m) +"x") 
                    if c > 0:
                        print("y="+ str(m) +"x + "+ str(c)) 
                    if c < 0:
                        print("y="+ str(m) +"x "+ str(c)) 



        #shi-Tomasi corner detection
        #23
        corners = cv.goodFeaturesToTrack(gray_image1, 12 , 0.01, 10)
        corners = np.int0(corners) 
        print(corners)

        listPoint = [[0] * colP for i in range(0,len(corners))]
        print("corners=",len(corners))
        # draw pink color circles on all corners 
        for i in corners: 
            xpoint, ypoint = i.ravel() 
            
            cv.circle(cdstP, (xpoint, ypoint), 3, (255, 0, 255), -1)
            
            for i in range(0,len(corners)):
                ls = corners[i][0]
                if (i==0 or i<=len(corners)):
                    listPoint[i][0] = ls[0]
                    listPoint[i][1] = ls[1]

            #print(listPoint)
            
            if(ynew1 == ypoint or ynew2 == ypoint or ynew3 == ypoint):
                print("on the same y")
            elif(xnew1 == xpoint or xnew2 == xpoint or xnew3 == xpoint):
                print("on the same x")
            
            #if((ynew1 != ypoint and xnew1 != xpoint) or (ynew2 != ypoint and xnew2 != xpoint) or (ynew3 != ypoint and xnew3 != xpoint)):
            else:
                p1 = (ynew1 -ynew3)/(xnew1 -xnew3)
                n1=round(p1)

                p2 = (ynew1 -ynew2)/(xnew1 -xnew2)
                n2=round(p2)

                p3 = (ynew2 -ynew3)/(xnew2 -xnew3)
                n3=round(p3)

                if((ynew1 != ypoint and xnew1 != xpoint) or (ynew2 != ypoint and xnew2 != xpoint) or (ynew3 != ypoint and xnew3 != xpoint)):
                    q1 = (ynew1 - ypoint)/(xnew1 - xpoint)
                    m1=round(q1)

                    q2 = (ynew1 - ypoint)/(xnew1 - xpoint)
                    m2=round(q2)

                    q3 = (ynew3 - ypoint)/(xnew3 - xpoint)
                    m3=round(q3)
                    #cross = dxc * dyl - dyc * dxl
                
                # print("n1= ",n1)
                # print("m1= ",m1)
                # print("n3= ",n3)
                # print("m3= ",m3)

                # print("===============================")
                # print(" ")

                if (n1 != m1 or n2 != m2 or n3 != m3):
                    print("no")   
                
                #identify small line segments in the middle of the lines and mark them as red dots
                for j in range(0,len(corners)):  
                    if((n1 == m1 or n1==(-m1)) and ((listPoint[j][1]<=((ynew1 -ynew3)/2)+ynew3+10) and (listPoint[j][1]>=((ynew1 -ynew3)/2)-10+ynew3)) and ((listPoint[j][0]<=((xnew1 -xnew3)/2)+10+xnew3) and (listPoint[j][0]>=((xnew1 -xnew3)/2)-10+xnew3))):
                        cv.circle(cdstP, (listPoint[j][0], listPoint[j][1]), 3, (0, 0, 255), -1)
                        a = 1

                    if((n3 == m3 or n3==(-m3)) and ((listPoint[j][1]<=((ynew2 -ynew3)/2)+ynew3+10) and (listPoint[j][1]>=((ynew2 -ynew3)/2)-10+ynew3)) and ((listPoint[j][0]<=((xnew3 -xnew2)/2)+10+xnew2) and (listPoint[j][0]>=((xnew3 -xnew2)/2)-10+xnew2))):
                        cv.circle(cdstP, (listPoint[j][0], listPoint[j][1]), 3, (0, 0, 255), -1)
                        b = 1

                    if((n2 == m2 or n2==(-m2)) and ((listPoint[j][1]<=((ynew2 -ynew1)/2)+ynew1+10) and (listPoint[j][1]>=((ynew2 -ynew1)/2)-10+ynew1)) and ((listPoint[j][0]<=((xnew1 -xnew2)/2)+10+xnew2) and (listPoint[j][0]>=((xnew1 -xnew2)/2)-10+xnew2))):
                        cv.circle(cdstP, (listPoint[j][0], listPoint[j][1]), 3, (0, 0, 255), -1)
                        c = 1
               

        #get the gradients of each line         
        e = (ynew2-ynew1)/(xnew2-xnew1)
        f = (ynew3-ynew1)/(xnew3-xnew1)
        g = (ynew3-ynew2)/(xnew3-xnew2)

        #multiply gradients of two lines
        ef = round(e*f)
        eg = round(e*g)
        fg = round(f*g)
        print("ef", ef)
        print("eg", eg)
        print("fg", fg)

        #put the multiplied gradients to a list called gradprod
        gradprod = [ef,eg,fg]


      #*********************************************************************************************************************************************************
        list = ['temp3.png','temp4.png','temp5.png', 't_12_1.png', 't_12_2.png','t_13_1.png', 't_13_2.png', 't_13_3.png', 't_14_1.png','t_14_2.png', 't_15_1.png', 't_16_1.png', 't_17_1.png', 't_17_2.png', 't_18_1.png', 't_20_2.png', 't_21_1.png', 't_21_2.png', 't_21_3.png', 't_23_1.png', 't_23_2.png', 't_23_3.png','t_26_1.png', 't_77_1.png', 't_77_2.png',  't_78_1.png', 't_78_2.png',  't_78-1_1.png', 't_78-2_1.png', 't_78-2_2.png', 't_86_1.png', 't_87_1.png', 't_87_2.png', 't_89_1.png', 't_94_1.png', 't_94_2.png', 't_95-1_1.png', 't_95-2_1.png', 't_95-3_1.png', 't_95-3_2.png', 't_2000_1.png', 't_2003_1.png', 't_2003_2.png', 't_2003_3.png', 't_2007_1.png', 't_2012_1.png', 't_2012_2.png', 't_2013_1.png', 't_2013_2.png', 't_2013_3.png', 't_2018_1.png', 't_2018_2.png', 't_2019_1.png', 't_2019_2.png', 't_2019_3.png', 't_2019-1_1.png', 't_2019-1_2.png', 'T_18.png', 'T_10.png', 'T_10_1.png', 'T_11_1.png', 'T_11_1.png', 'td_1_2.png', 'td_2_1.png', 'td_2_2.png', 'td_3_1.png', 'td_3_2.png', 'td_4_1.png', 'td_4_2.png', 'td_5_1.png', 'td_5_2.png', 't_2008_1.png', 't_scal3.png', 't_scal5.png',  'tsd3-1.png', 'tsd3-2.png', 'tsd4-1.png', 'tsd4-2.png', 'tsd5-1.png', 'tsd5-2.png', 'tsd6-1.png', 'tsd6-2.png', 'k1t1.png', 'k1t2.png', 'k2t1.png', 'a1t1.png', 'a2t1.png', 'a3t1.png', 'a3t2.png', 'a4t1.png', 'a4t2.png', 'a5t1.png', 'a6t1.png', 'a6t2.png', 'a7t1.png', 'a7t2.png', 'a7t3.png', 'a8t1.png', 'a8t2.png', 'a10t1.png', 'a10t2.png', 'a10t3.png', 'a11t1.png', 'a11t2.png', 'a12t1.png', 'a12t2.png', 'a13t1.png', 'a14t1.png', 'a14t2.png', 'a15t1.png', 'a15t2.png', 'a16t1.png', 'a17t1.png', 'a17t2.png', 'a18t1.png', 'a18t2.png', 'k3t1.png', 'k3t2.png', 'k6t1.png', 'k6t2.png', 'k7t1.png', 'k15t1.png', 'k15t2.png', 'k16t1.png', 'k16t2.png', 'k5t1.png', 'k5t2.png', 't_27_1.png', 't_27_2.png', 't_28_1.png', 't_28_2.png', 'k10t1.png', 'k10t2.png', 'k12t1.png', 'draw_6_t1.png', 'draw_6_t2.png']
        #, 't_77_1.png', 't_77_2.png',  , 't_78-1_1.png', 't_78-2_1.png', 't_78-2_2.png', 't_86_1.png', 't_87_1.png', 't_87_2.png', 't_89_1.png', 't_94_1.png', 't_95-1_1.png', 't_95-2_1.png', 't_95-3_1.png', 't_95-3_2.png', 't_2000_1.png', 't_2003_1.png', 't_2003_2.png', 't_2007_1.png', 't_2012_1.png', 't_2012_2.png', 't_2013_1.png', 't_2013_2.png', 't_2013_3.png', 't_2018_1.png', 't_2018_2.png', 't_2019_1.png', 't_2019_2.png', 't_2019-1_1.png', 't_2019-1_2.png' , 'k12t2.png'
        num1 = num2 = num3 = 0
        let1 = let2 = let3 = ''
        for imageT in list:
            template = cv.imread(imageT,0)
            w, h = template.shape[::-1]

            res = cv.matchTemplate(gray_image,template,cv.TM_CCOEFF_NORMED)
            threshold = 0.8
            loc = np.where( res >= threshold)

            for pt in zip(*loc[::-1]):
                cv.rectangle(src, pt, (pt[0] + w, pt[1] + h), (0,0,255), 2)
                print((pt[0], pt[0] + w, pt[1], pt[1] + h))
                listTemp = [[pt[0], pt[1]], [pt[0] + w, pt[1] + h]] 
                print(listTemp)
                custom_config = r'-l eng --oem 3 --psm 6'
                result=pytesseract.image_to_string(imageT, config=custom_config)
                print("**********",result)

                #&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&
                #identify the values corresponding to the cordinates of the intersection points/corners

                val1 = pow(((pt[0] + w) - xnew1),2) + pow(((pt[1] + h) - ynew1),2)
                val2 = pow(((pt[0] + w) - xnew2),2) + pow(((pt[1] + h) - ynew2),2)
                val3 = pow(((pt[0] + w) - xnew3),2) + pow(((pt[1] + h) - ynew3),2) 
                print("val1",val1)
                print("val2",val2)
                print("val3",val3)
                absval1 = abs(val1)
                absval2 = abs(val2)
                absval3 = abs(val3)
                minval = min(absval1,absval2,absval3)
                
                print("minval",minval)
                #pink => if minval becomes absolute value1, then that point of the template is corresponding to (xnew1,ynew1) coordinate
                if (minval == absval1):
                    cv.circle(src, (pt[0] + w, pt[1] + h), 3, (255, 0, 255), -1)
                    cv.circle(src, (xnew1,ynew1), 3, (255, 0, 255), -1)
                    print("**aaa****",result)
                    if result >='a'  and result <='z':
                        let = result
                        print("letter",let)
                        let1=let
                    elif int(result)>0 and int(result) <360:
                        num1 = int(result)
                        print("num1",num1)
                    
                #blue => if minval becomes absolute value2, then that point of the template is corresponding to (xnew2,ynew2) coordinate
                if (minval == absval2):
                    cv.circle(src, (pt[0] + w, pt[1] + h), 3, (255, 0, 100), -1)
                    cv.circle(src, (xnew2,ynew2), 3, (255, 0, 100), -1)
                    print("**bbb****",result)
                    if result >='a'  and result <='z':
                        let = result
                        print("letter",let)
                        let2=let
                    elif int(result)>0 and int(result) <360:
                        num2 = int(result)
                        print("num2",num2)
                    

                #yellow => if minval becomes absolute value3, then that point of the template is corresponding to (xnew3,ynew3) coordinate
                if (minval == absval3):
                    cv.circle(src, (pt[0] + w, pt[1] + h), 3, (0,255,255), -1)
                    cv.circle(src, (xnew3,ynew3), 3, (0,255,255), -1)
                    print("**ccc****",result)
                    if result >='a'  and result <='z':
                        let = result
                        print("letter",let)
                        let3=let
                    elif int(result)>0 and int(result) <360:
                        num3 = int(result)
                        print("num3",num3)

            #&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&


                # A utility function to calculate area  
                # of triangle formed by (x1, y1),  
                # (x2, y2) and (x3, y3) 
                
                #def area(xnew1, ynew1, xnew2, ynew2, xnew3, ynew3): 
                
                    #return abs((xnew1 * (ynew2 - ynew3) + xnew2 * (ynew3 - ynew1) + xnew3 * (ynew1 - ynew2)) / 2.0) 
                
                
                # check whether point P(x, y) 
                # lies inside the triangle formed by  
                # A(x1, y1), B(x2, y2) and C(x3, y3)  
                if result>='a':        
                            # Calculate area of triangle ABC 
                    A = abs((xnew1 * (ynew2 - ynew3) + xnew2 * (ynew3 - ynew1) + xnew3 * (ynew1 - ynew2)) / 2.0)
                            
                                # Calculate area of triangle PBC  
                                #A1 = area ( pt[0]+w, pt[1]+h, xnew2, ynew2, xnew3, ynew3) 
                    A1 = abs(((pt[0]+w) * (ynew2 - ynew3) + xnew2 * (ynew3 - (pt[1]+h)) + xnew3 * ((pt[1]+h) - ynew2)) / 2.0)
                                
                                # Calculate area of triangle PAC  
                                #A2 = area (xnew1, ynew1,  pt[0]+w, pt[1]+h, xnew3, ynew3) 
                    A2 = abs((xnew1 * ((pt[1]+h) - ynew3) + (pt[0]+w) * (ynew3 - ynew1) + xnew3 * (ynew1 - (pt[1]+h))) / 2.0)
                                
                                # Calculate area of triangle PAB  
                                #A3 = area (xnew1, ynew1, xnew2, ynew2,  pt[0]+w, pt[1]+h) 
                    A3 = abs((xnew1 * (ynew2 - (pt[1]+h)) + xnew2 * ((pt[1]+h) - ynew1) + (pt[0]+w) * (ynew1 - ynew2)) / 2.0)
                                # Check if sum of A1, A2 and A3  
                                # is same as A 
                    if(A == A1 + A2 + A3): 
                        print('Letter Inside Triangle')
                    else: 
                        print('Letter Not Inside Triangle')

                elif int(result) >= 1:
                    An = abs((xnew1 * (ynew2 - ynew3) + xnew2 * (ynew3 - ynew1) + xnew3 * (ynew1 - ynew2)) / 2.0)
                            
                                # Calculate area of triangle PBC  
                                #A1 = area ( pt[0]+w, pt[1]+h, xnew2, ynew2, xnew3, ynew3) 
                    An1 = abs(((pt[0]+w) * (ynew2 - ynew3) + xnew2 * (ynew3 - (pt[1]+h)) + xnew3 * ((pt[1]+h) - ynew2)) / 2.0)
                                
                                # Calculate area of triangle PAC  
                                #A2 = area (xnew1, ynew1,  pt[0]+w, pt[1]+h, xnew3, ynew3) 
                    An2 = abs((xnew1 * ((pt[1]+h) - ynew3) + (pt[0]+w) * (ynew3 - ynew1) + xnew3 * (ynew1 - (pt[1]+h))) / 2.0)
                                
                                # Calculate area of triangle PAB  
                                #A3 = area (xnew1, ynew1, xnew2, ynew2,  pt[0]+w, pt[1]+h) 
                    An3 = abs((xnew1 * (ynew2 - (pt[1]+h)) + xnew2 * ((pt[1]+h) - ynew1) + (pt[0]+w) * (ynew1 - ynew2)) / 2.0)
                                # Check if sum of A1, A2 and A3  
                                # is same as A 
                    if(An == An1 + An2 + An3): 
                        print('Number Inside Triangle')
                    else: 
                        print('Number Not Inside Triangle')
                
                


      #**********************************************************************************************************

        #EQUILATERAL TRIANGLES
        if(a == b == c):
            print("Equilateral")
            if(A == A1 + A2 + A3):
                angle = 180/3
                print(let,"=",angle)
            else:
                angle = 180 - 60
                print(let,"=",angle)


        #ISOSCELES TRIANGLES
        elif((a == b) or (a == c) or (b == c)):
            print("Isosceles")           
            
            #identify right angled triangles if product of 2 gradients is equal to -1
            for j in range (0,3): 
                #if multiplication of two gradients is -1, then there's a right angle
                if(gradprod[j] == -1):
                    print(j,gradprod[j])
                    print("Right angled triangle")

                    if(A == A1 + A2 + A3): 
                        angle = 90/2
                        print(let,"=",angle)
                    else:
                        angle = 180 - 45
                        print(let,"=",angle)
                    #get the coordinates of lines that make the right angle
                    if (j==0):
                        print(((xnew1,ynew1),(xnew2,ynew2)),((xnew1,ynew1),(xnew3,ynew3)))
                    elif (j==1):
                        print(((xnew1,ynew1),(xnew3,ynew3)),((xnew2,ynew2),(xnew3,ynew3)))
                    elif (j==2):
                        print(((xnew2,ynew2),(xnew3,ynew3)),((xnew1,ynew1),(xnew3,ynew3)))
                        
            #if not a right angled triangle
            else:
                if(a == b):
                    #when a=b, intersection point is(xnew3,ynew3).then the nearest number is num3 
                    print("x3",xnew3)
                    print("y3",ynew3)
                    print("tttttt3")
                    cv.circle(src, (xnew3, ynew3), 3, (0, 0, 255), -1)

                    #when there is a number near to the intersection point of the equal sides
                    if(num3>0):
                        #if the unkown letter is inside the triangle
                        if(A == A1 + A2 + A3):
                            #num also inside
                            if (An == An1 + An2 + An3):
                                angle = (180 - num3)/2
                                print(let,"=",angle)
                                print('jjjjjjjj')
                            #num outside
                            else:
                                angle = num3/2
                                print(let,"=",angle)
                        #if the unkown letter is outside the triangle
                        else:
                            #num inside
                            if (An == An1 + An2 + An3):
                                angle = ((180-num3)/2) + num3
                                print(let,"=",angle)
                            #num outside
                            else:
                                angle = 180-(num3/2) 
                                print(let,"=",angle)
                            
                    # when there is an unknown letter near to the intersection point of the equal sides
                    elif(num3 == 0 and let3>='a'):
                        if(A == A1 + A2 + A3):
                            if(num2>0):
                                angle = (180 - 2*num2)
                                print(let,"=",angle)
                            elif(num1>0):
                                angle = (180 - 2*num1)
                                print(let,"=",angle)
                        #when the unknown letter near the intersection point of the equal sides and is outside the triangle
                        else:
                            if(num2>0):
                                angle = (2*num2)
                                print(let,"=",angle)
                            elif(num1>0):
                                angle = (2*num1)
                                print(let,"=",angle)

                    #when there is no number or no letter near to the intersection point of the equal sides
                    elif(num3 == 0 and let3<='a'):
                        if(A == A1 + A2 + A3):
                            if(num1>0):
                                angle = num1
                                print(let,"=",angle)
                            elif(num2>0):
                                angle = num2
                                print(let,"=",angle)
                        else:
                            if(num1>0):
                                angle = 180 - num1
                                print(let,"=",angle)
                                print('++++++')
                            elif(num2>0):
                                angle = 180 - num2
                                print(let,"=",angle)
                                print('-------')
                
                elif(a == c):
                    print("x1",xnew1)
                    print("y1",ynew1)
                    print("ssssss3")
                    cv.circle(src, (xnew1, ynew1), 3, (0, 0, 255), -1)
                    #when there is a number near to the intersection point of the equal sides
                    
                    if(num1>0):   #num1 is the nearest number to the intersection point (xnew1,ynew1)
                        if(A == A1 + A2 + A3):
                            #num also inside
                            if (An == An1 + An2 + An3):
                                angle = (180 - num1)/2
                                print(let,"=",angle)
                                print('jjjjjjjj')
                            #num outside
                            else:
                                angle = num1/2
                                print(let,"=",angle)
                        #if the unkown letter is outside the triangle
                        else:
                            #num inside
                            if (An == An1 + An2 + An3):
                                angle = ((180-num1)/2) + num1
                                print(let,"=",angle)
                            #num outside
                            else:
                                angle = 180-(num1/2) 
                                print(let,"=",angle)


                    #when there is a unknown letter near to the intersection point of the equal sides
                    elif(num1 == 0 and let1>='a'):
                        #???????????what if inside and outside triangle
                        if(num2>0):
                            angle = (180 - 2*num2)
                            print(let,"=",angle)
                        elif(num3>0):
                            angle = (180 - 2*num3)
                            print(let,"=",angle)
                    
                    elif(num1 == 0 and let1<='a'):
                        if(num2>0):
                            angle = num2
                            print(let,"=",angle)
                        elif(num3>0):
                            angle = num3
                            print(let,"=",angle)

                    #when there is no number or no letter near to the intersection point of the equal sides(modified 04.18)
                    elif(num1 == 0 and let1<='a'):
                        if(A == A1 + A2 + A3):
                            if(num3>0):
                                angle = num3
                                print(let,"=",angle)
                            elif(num2>0):
                                angle = num2
                                print(let,"=",angle)
                        else:
                            if(num3>0):
                                angle = 180 - num3
                                print(let,"=",angle)
                                print('++++++')
                            elif(num2>0):
                                angle = 180 - num2
                                print(let,"=",angle)
                                print('-------')  
                    ##up to here  (modified 04.18)    

                elif(b == c):
                    print("x2",xnew2)
                    print("y2",ynew2)
                    #print("rrrrrr3")
                    cv.circle(src, (xnew2, ynew2), 3, (0, 0, 255), -1)
                    #when there is a number near to the intersection point of the equal sides
                    if(num2>0):
                        if(A == A1 + A2 + A3):
                            #num also inside
                            if (An == An1 + An2 + An3):
                                angle = (180 - num2)/2
                                print(let,"=",angle)
                                print('jjjjjjjj')
                            #num outside
                            else:
                                angle = num2/2
                                print(let,"=",angle)
                        #if the unkown letter is outside the triangle
                        else:
                            #num inside
                            if (An == An1 + An2 + An3):
                                angle = ((180-num2)/2) + num2
                                print(let,"=",angle)
                            #num outside
                            else:
                                angle = 180-(num2/2) 
                                print(let,"=",angle)


                    elif(num2 == 0 and let2>='a'):
                        if(A == A1 + A2 + A3):
                            if(num3>0):
                                angle = (180 - 2*num3)
                                print(let,"=",angle)
                            elif(num1>0):
                                angle = (180 - 2*num1)
                                print(let,"=",angle)
                        else:
                            if(num3>0):
                                angle = (2*num3)
                                print(let,"=",angle)
                            elif(num1>0):
                                angle = (2*num1)
                                print(let,"=",angle)

                    elif(num2 == 0 and let2<='a'):
                        if(A == A1 + A2 + A3):
                            if(num1>0):
                                angle = num1
                                print(let,"=",angle)
                            elif(num3>0):
                                angle = num3
                                print(let,"=",angle)
                        else:
                            if(num1>0):
                                angle = (180 - num1)    #modified 18.04
                                print(let,"=",angle)
                            elif(num3>0):
                                angle = (180 - num3)   #modified 18.04
                                print(let,"=",angle)


        #SCALENE TRIANGLE          
        elif(a != b != c):
            print("Scalene")
            #++++++++
        
            for j in range (0,3): 
                if(gradprod[j] == -1):
                    print(j,gradprod[j])
                    print("Right angled triangle")

                    if(A == A1 + A2 + A3):
                        #num also inside
                        if (An == An1 + An2 + An3):
                            #get the value of the unknown angle
                            #num1 comes from (xnew1,ynew1)
                            if num1 > 0:
                                angle = 90 - num1
                                print(let,"=",angle)
                            #num2 comes from (xnew2,ynew2)
                            if num2 > 0:
                                angle = 90 - num2
                                print(let,"=",angle)
                            #num3 comes from (xnew3,ynew3)
                            if num3 > 0:
                                angle = 90 - num3
                                print(let,"=",angle)
                        else:
                            #num1 comes from (xnew1,ynew1)
                            if num1 > 0:
                                angle = num1 - 90
                                print(let,"=",angle)
                            #num2 comes from (xnew2,ynew2)
                            if num2 > 0:
                                angle = num2 - 90
                                print(let,"=",angle)
                            #num3 comes from (xnew3,ynew3)
                            if num3 > 0:
                                angle = num3 - 90
                                print(let,"=",angle) 
                    
                    else:
                        if num1 > 0:
                            angle = 90 + num1
                            print(let,"=",angle)
                        #num2 comes from (xnew2,ynew2)
                        if num2 > 0:
                            angle = 90 + num2
                            print(let,"=",angle)
                        #num3 comes from (xnew3,ynew3)
                        if num3 > 0:
                            angle = 90 + num3
                            print(let,"=",angle)

            #get the angles of non-right angled scelene triangles
            else:
                if(A == A1 + A2 + A3):
                    if num1>0 and num2>0:
                        angle = 180 - (num1 + num2)
                        print(let,"=",angle)
                    elif num1>0 and num3>0:
                        angle = 180 - (num1 + num3)
                        print(let,"=",angle)
                    elif num2>0 and num3>0:
                        angle = 180 - (num2 + num3)
                        print(let,"=",angle)
                
                else:
                    if num1>0 and num2>0:
                        angle = (num1 + num2)
                        print(let,"=",angle)
                    elif num1>0 and num3>0:
                        angle = (num1 + num3)
                        print(let,"=",angle)
                    elif num2>0 and num3>0:
                        angle = (num2 + num3)
                        print(let,"=",angle)
                

        
                #  print("Angle=",angle_s)
                    #get the coordinates of lines that make the right angle
                if (j==0):
                    print(((xnew1,ynew1),(xnew2,ynew2)),((xnew1,ynew1),(xnew3,ynew3)))
                elif (j==1):
                    print(((xnew1,ynew1),(xnew3,ynew3)),((xnew2,ynew2),(xnew3,ynew3)))
                elif (j==2):
                    print(((xnew2,ynew2),(xnew3,ynew3)),((xnew1,ynew1),(xnew3,ynew3)))
                    
            
                 
           
    if linesP is not None: # Check there are lines


     
        storeLineCoordinate()
        generateLineEquation()

        # Show results
    cv.imshow("Source", src)
    cv.imshow("Probabilistic Line Transform", cdstP)
    cv.imshow("Canny edge", dst)
    
    cv.waitKey()
    return 0

if __name__ == "__main__":
   main(sys.argv[1:])


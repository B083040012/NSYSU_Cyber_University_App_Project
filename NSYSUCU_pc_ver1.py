# Import class "My_webdriver" (Including chrome_option)
from Chrome_webdriver import My_Webdriver,WebDriverWait,EC,By
# Import class "My_Google_Drive" (Including search_folder,file_upload function)
from Google_Drive_API import My_Google_Drive
from time import sleep
import os
from math import floor
import requests

Browser=My_Webdriver()
Upload_Function=My_Google_Drive()

class NSYSUCU:
    def __init__(self):
        # Import chrome setting,return driver
        self.driver=Browser.set_options()
        # Get url,go to website
        try:
            self.driver.get('https://cu.nsysu.edu.tw/mooc/login.php')
        # if the account didn't logout (get error) ,logout first
        except:
            self.driver.find_element_by_xpath("//*[@id='div_username']/table/tbody/tr/td[2]/a").click()
            self.driver.implicitly_wait(2)
            self.driver.find_element_by_xpath("//*[@id='div_username']/table/tbody/tr/td/input").click()

    def Message_Board(self,*message,length):
        # Login page
        if message[0]=="login":
            print("========================================================================")
            print("==                                                                    ==")
            print("==                 Welcome to NSYSU Cyber University!                 ==")
            print("==                 ==================================                 ==")
            print("==                              Log in...                             ==")
            print("==                                                                    ==")
            print("========================================================================")
        else:
            print("================================================")
            for i in range(3):
                print("=====                                      =====")
            # "Input wrong number" page
            if message[0]=="Wrong number":
                print("          Wrong number!(Enter 0~%d)             "%(length))
            # Course page
            elif message[0]=="course page":
                for i in range(floor((35-len(message[1]))/2)):
                    print(" ",end='')
                print("Now on:",message[1])
                print("              =================")
                print("              1.Course Messages",end='')
                print("\n              2.Course Document")
                print("                   0.Exit")
            else:
                # Other message(s)
                for sentance in message:
                    for i in range(floor((48-len(sentance))/2)):
                        print(" ",end='')
                    print(sentance)
            for i in range(3):
                print("=====                                      =====")
            print("================================================")

    def Select_Function(self,sel_message,length_of_list):
        try:
            # Check if input is a number or not
            sel=int(input(sel_message))
        except:
            # If input is not a number
            os.system("cls")
            self.Message_Board("Illegal character!","Please enter a number.",length=0)
            sleep(1)
            return -1
        else:
            # Input out of range
            if sel>length_of_list or sel<0:
                os.system("cls")
                self.Message_Board("Wrong number",length=length_of_list)
                sleep(1)
                return -1
            return sel

    def Course_Info_Check(self):
        message_empty=False
        document_empty=False
        # Check message page is empty or not
        self.driver.switch_to.default_content()
        self.driver.switch_to.frame(self.driver.find_element_by_name("s_main"))
        self.driver.implicitly_wait(5)
        try:
            message_empty_detect=self.driver.find_element_by_xpath("//table[@id='news-tpc']")
        except:
            sleep(3)
            message_empty_detect=self.driver.find_element_by_xpath("//table[@id='news-tpc']")
        message_empty_detect=message_empty_detect.find_elements_by_xpath(".//div[@class='title']")
        if message_empty_detect[0].text=="目前無文章":
            message_empty=True
        # Check document page is empty or not
        self.driver.switch_to.default_content()
        self.driver.switch_to.frame(self.driver.find_element_by_name("mooc_sysbar"))
        self.driver.find_element_by_xpath("//a[@id='SYS_04_01_002']").click()
        self.driver.switch_to.default_content()
        self.driver.switch_to.frame(self.driver.find_element_by_name("s_catalog"))
        self.driver.implicitly_wait(2)
        self.driver.switch_to.frame(self.driver.find_element_by_name("pathtree"))
        document_empty_detect=self.driver.find_elements_by_xpath("//div[not(@class)][not(@id)][@style]")
        if len(document_empty_detect)==0:
            document_empty=True
            if message_empty==False:
                # If document page is empty but message page is not,return to message page
                self.driver.switch_to.default_content()
                self.driver.switch_to.frame(self.driver.find_element_by_name("mooc_sysbar"))
                self.driver.find_element_by_xpath("//a[@id='SYS_04_01_001']").click()
        return message_empty,document_empty

    def File_Download_Upload(self,course_name):
        try:
            # Check if there is file or not
            file_info=self.driver.find_element_by_xpath("//div[@class='file']")
        except:
            # No file
            input("No file in this post,press any button to exit")
            self.driver.find_element_by_xpath("//a[@title='回列表']").click()
            return
        else:
            # Find all file(s) information
            file_download=file_info.find_elements_by_xpath(".//a[@class='attach-file-link']")
            file_capacity=file_info.find_elements_by_xpath(".//span[not(@class)]")
            print("\n\nFile(s) to download:")
            for (file_num,file_name),file_byte in zip(enumerate(file_download),file_capacity):
                print(str(file_num+1)+":",file_name.text+file_byte.text)
            while(1):
                try:
                    sel_file=int(input("Select file to download:(Enter 0 to exit):"))
                except:
                    print("Please enter a number")
                else:
                    if sel_file==0:
                        self.driver.find_element_by_xpath("//a[@title='回列表']").click()
                        return
                    elif sel_file<0 or sel_file>len(file_download):
                        print("Wrong number!")
                    else:
                        # Executing download/upload process
                        current_file=file_download[sel_file-1].text
                        file_download[sel_file-1].click()
                        print("===============================\n")
                        print('File downloading...'+"("+current_file+")")
                        while(not(os.path.isfile(Browser.download_path+"\\"+current_file))):
                            sleep(0.5)
                        print(current_file," download complete!")
                        upload_file_sel=input("Upload this file? Y(yes) or any other button(No)")
                        if upload_file_sel=="y" or upload_file_sel=="Y" or upload_file_sel=="yes" or upload_file_sel=="Yes":
                            Upload_Function.file_upload(True,current_file,Browser.download_path+"/",course_name)
                        print("\n===============================\n")
        
    def Message_Info(self,course_name):
        # Find/print message information(Author,Time,Content)
        post_info=self.driver.find_element_by_xpath("//div[@class='top-tmp']")
        post_name=post_info.find_element_by_xpath(".//div[@class='author-name']")
        post_time=post_info.find_element_by_xpath(".//div[@class='post-time']")
        content=self.driver.find_element_by_xpath("//div[@class='bottom-tmp']")
        content=content.find_elements_by_xpath(".//p")
        print("Author:",post_name.text)
        print("Time:",post_time.text)
        print("Content:",end='')
        for sub_content in content:
            print(sub_content.text)
        # Download/upload process
        self.File_Download_Upload(course_name)

    def Login(self,stu_num,password):
        os.system("cls")
        self.Message_Board("login",length=0)
        username_input=self.driver.find_element_by_css_selector('input[placeholder="帳號"]')
        username_input.send_keys(stu_num)
        password_input=self.driver.find_element_by_css_selector('input[placeholder="密碼"]')
        password_input.send_keys(password)
        logbutton=self.driver.find_element_by_id('btnSignIn')
        logbutton.click()

    def Course_Select_List(self):
        # Get into the frame and get all the course names/links
        self.driver.switch_to.default_content()
        self.driver.switch_to.frame(self.driver.find_element_by_name("mooc_sysbar"))
        all_course=self.driver.find_elements_by_tag_name('option')
        while(1):
            os.system("cls")
            # Course selecting page
            print(all_course[0].text,":")
            for (num_course,course) in enumerate(all_course[1:]):
                print(str(num_course+1)+":",course.text[5:])
            sel_course=self.Select_Function("PLease select the course (Enter 0 to exit):",len(all_course)-1)
            if sel_course==-1:
                continue
            elif sel_course==0:
                # Exit
                return sel_course,"None"
            course_name=all_course[sel_course].text[5:]
            all_course[sel_course].click()
            break
        return sel_course,course_name

    def Auto_Course_Select_List(self,New_Detect):
        # Select course list automatically by while loop
        i=1
        while(i<=10):
            self.driver.switch_to.default_content()
            self.driver.switch_to.frame(self.driver.find_element_by_name("mooc_sysbar"))
            all_course=self.driver.find_elements_by_tag_name('option')
            course_name=all_course[i].text[5:]
            all_course[i].click()
            self.Auto_Course_Page(course_name,New_Detect)
            i+=1

    def Course_Page(self,course_name,course_num):
        # Check if message/document page is empty or not
        message_empty,document_empty=self.Course_Info_Check()
        while(1):
            if message_empty==True and document_empty==True:
                os.system("cls")
                self.Message_Board("No message and document in "+course_name+",","Press any button to exit.",length=0)
                input()
                break
            elif message_empty==False and document_empty==False:
                os.system("cls")
                self.Message_Board("course page",course_name,message_empty,length=0)
                sel_course_function=self.Select_Function("Please select function:",2)
                os.system("cls")
                self.Message_Board("Loading...",length=0)
                if sel_course_function==0:
                    break
                elif sel_course_function==1:
                    try:
                        self.driver.switch_to.default_content()
                        self.driver.switch_to.frame(self.driver.find_element_by_name("s_main"))
                        self.driver.implicitly_wait(2)
                        self.driver.find_element_by_xpath("//*[@id='pageToolbar']/div[1]")
                        self.Course_Message(course_name,False)
                    except:
                        self.driver.switch_to.default_content()
                        self.driver.switch_to.frame(self.driver.find_element_by_name("mooc_sysbar"))
                        self.driver.find_element_by_xpath("//a[@id='SYS_04_01_001']").click()
                        self.driver.implicitly_wait(2)
                        self.Course_Message(course_name,False)
                elif sel_course_function==2:
                    self.driver.switch_to.default_content()
                    self.driver.switch_to.frame(self.driver.find_element_by_name("mooc_sysbar"))
                    self.driver.find_element_by_xpath("//a[@id='SYS_04_01_002']").click()
                    self.Course_Document(course_name)
            elif document_empty==True:
                self.Course_Message(course_name,False)
                break
            else:
                self.Course_Document(course_name)
                break

    def Auto_Course_Page(self,course_name,new_detect):
        # Select course info by checking if the message or document is empty or not
        os.system("cls")
        self.Message_Board("Now on : "+course_name+"...","Loading...",length=0)
        self.driver.switch_to.default_content()
        self.driver.switch_to.frame(self.driver.find_element_by_name("s_main"))
        self.driver.implicitly_wait(5)
        try:
            message_empty_detect=self.driver.find_element_by_xpath("//table[@id='news-tpc']")
        except:
            sleep(3)
            message_empty_detect=self.driver.find_element_by_xpath("//table[@id='news-tpc']")
        message_empty_detect=message_empty_detect.find_elements_by_xpath(".//div[@class='title']")
        if message_empty_detect[0].text=="目前無文章":
            message_empty=True
        else:
            message_empty=False
            self.Course_Message(course_name,new_detect)
        self.driver.switch_to.default_content()
        self.driver.switch_to.frame(self.driver.find_element_by_name("mooc_sysbar"))
        self.driver.find_element_by_xpath("//a[@id='SYS_04_01_002']").click()
        self.driver.switch_to.default_content()
        self.driver.switch_to.frame(self.driver.find_element_by_name("s_catalog"))
        self.driver.implicitly_wait(2)
        self.driver.switch_to.frame(self.driver.find_element_by_name("pathtree"))
        document_empty_detect=self.driver.find_elements_by_xpath("//div[not(@class)][not(@id)][@style]")
        if len(document_empty_detect)==0:
            if message_empty==True:
                os.system("cls")
                self.Message_Board("No message and document in "+course_name+".",length=0)
                sleep(0.5)
            return
        else:
            self.Course_Document(course_name)
            
    def Course_Message(self,course_name,new_detect):
        while(1):
            os.system("cls")
            self.Message_Board("Loading...",length=0)
            self.driver.implicitly_wait(2)
            self.driver.switch_to.default_content()
            self.driver.switch_to.frame(self.driver.find_element_by_name("s_main"))
            self.driver.implicitly_wait(2)
            # Set the number of message that show on the window (10 -> 400)
            page_tool=self.driver.find_element_by_xpath("//select[@class='paginate-list']")
            page_tool.click()
            self.driver.implicitly_wait(2)
            more_message=self.driver.find_element_by_xpath("//option[@value='400']")
            more_message.click()
            page_tool.click()
            sleep(2)
            all_messages=self.driver.find_element_by_xpath("//table[@id='news-tpc']")
            all_messages=all_messages.find_elements_by_xpath(".//div[@class='title']")
            sel_message=-1
            if new_detect:
                new_message_detect=self.driver.find_element_by_xpath("//table[@id='news-tpc']")
                new_message_detect=new_message_detect.find_elements_by_xpath(".//td[@class='t2']")
                index=0
                for i in range(len(new_message_detect)):
                    try:
                        self.driver.implicitly_wait(1.5)
                        new_message_detect[i].find_element_by_xpath(".//div[@class='status ']")
                        del all_messages[index]
                    except:
                        index+=1
                    # try:
                    #     self.driver.implicitly_wait(2)
                    #     new_message_detect[i].find_element_by_xpath(".//div[@class='status new']")
                    #     index+=1    
                    # except:
                    #     del all_messages[index]
                if len(all_messages)==0:
                    os.system("cls")
                    self.Message_Board("No new message in "+course_name,length=0)
                    sleep(0.5)
                    return
            while(sel_message==-1):
                os.system("cls")
                print("Message(s) from "+course_name)
                for (num_message,message) in enumerate(all_messages):
                    # try:
                    #     if message.find_element_by_xpath(".//div[@class='status new']"):
                    #         print("!!!NEW!!!",str(num_message+1)+":",message.text)
                    # except:
                    print(str(num_message+1)+":",message.text)
                sel_message=self.Select_Function("Please select the message:(Enter 0 to exit):",len(all_messages))
            if sel_message==0:
                break
            else:
                os.system("cls")
                print("Title:",all_messages[sel_message-1].text)
                # Click the message
                self.driver.execute_script("arguments[0].click();", all_messages[sel_message-1])
                self.Message_Info(course_name)

    def Course_Document(self,course_name):
        while(1):
            # Find/print all the document
            self.driver.switch_to.default_content()
            self.driver.switch_to.frame(self.driver.find_element_by_name("s_catalog"))
            self.driver.switch_to.frame(self.driver.find_element_by_name("pathtree"))
            self.driver.implicitly_wait(0.5)
            document_info=self.driver.find_elements_by_xpath("//div[not(@class)][not(@id)][@style]")
            os.system("cls")
            print("Document(s) of "+course_name)
            for (docu_num,docu_name) in enumerate(document_info):
                print(str(docu_num+1)+":",docu_name.text)
            sel_document=self.Select_Function("Please select the document:(Enter 0 to exit):",len(document_info))
            if sel_document==0:
                return
            else:
                current_document=document_info[sel_document-1].text
                document_info[sel_document-1].click()
                os.system("cls")
                print("Document Loading..."+"("+current_document+")")
                self.driver.switch_to.default_content()
                self.driver.switch_to.frame(self.driver.find_element_by_name("s_main"))
                sleep(2)
                try:
                    # If the document is not .pdf
                    self.driver.implicitly_wait(2)
                    current_document=self.driver.find_element_by_xpath("/html/body/div[2]/div/form/div[1]").text
                    #find '(' character from behind -> rfind()
                    index=current_document.rfind('(')
                    current_document_byte=current_document[index:]
                    current_document=current_document[:index-1]
                    self.driver.find_element_by_xpath(".//button[@class='btn btn-large btn-blue']").click()
                except:
                    # If the document is .pdf
                    try:
                        # Wait the pdf page loading (until 100 sec)
                        sleep(3)
                        WebDriverWait(self.driver,100,0.5).until_not(EC.presence_of_element_located((By.CLASS_NAME, "loadingInProgress")))
                    except:
                        os.system("cls")
                        self.Message_Board("Loading out of time,please try again.",length=0)
                        sleep(1.5)
                        continue
                    else:
                        current_document=current_document+".pdf"
                        current_document_byte="(???MB)"
                        try:
                            self.driver.find_element_by_xpath(".//button[@id='download']").click()
                        except:
                            os.system("cls")
                            self.Message_Board("Document can't download or unexpected error\n",length=0)
                            sleep(2)
                            continue
                print("Document downloading..."+"("+current_document+str(current_document_byte)+")")
                # Check if the document is on your download_path or not 
                while(not(os.path.isfile(Browser.download_path+"\\"+current_document))):
                            sleep(0.5)
                print(current_document+" download complete!")
                upload_document_sel=input("Upload this document? Y(yes) or any other button(No)")
                if upload_document_sel=="y" or upload_document_sel=="Y" or upload_document_sel=="yes" or upload_document_sel=="Yes":
                    Upload_Function.file_upload(True,current_document,Browser.download_path,course_name)
                input("Press any button to exit")

    def Mode_Select(self):
        while(1):
            os.system("cls")
            self.Message_Board("Modes of NSYSUCU:","1.Manual Mode","2.Auto Mode","3.Auto Mode(Detect New)",length=0)
            mode_sel=self.Select_Function("Please select the mode (Press 0 to exit):",length_of_list=3)
            if mode_sel==-1:
                continue
            elif mode_sel==0:
                return
            elif mode_sel==1:
                while(1):
                    (current_course_num,current_course_name)=self.Course_Select_List()
                    if current_course_num==0:
                        break
                    self.Course_Page(current_course_name,current_course_num)
            elif mode_sel==2:
                self.Auto_Course_Select_List(False)
                break
            elif mode_sel==3:
                self.Auto_Course_Select_List(True)
                break

    def Progress(self):
        try:
            self.Login(<your_student_id>,<your_password>)
        except:
            try:
                if self.driver.find_element_by_xpath("//*[@id='main-message']/h1/span").text=="沒有網際網路連線":
                    os.system("cls")
                    self.Message_Board("Internet Error,Please try again",length=0)
                    sleep(1)
                    self.driver.close()
                    return
            except:
                os.system("cls")
                self.Message_Board("Unexpected Error,Please try again",length=0)
                sleep(1)
                self.driver.close()
                return
        self.Mode_Select()
        os.system("cls")
        self.Message_Board("See you next time!",length=0)
        self.driver.close()
        exit()

# modified from https://learn.markteaching.com/%E3%80%90google-api-%E6%95%99%E5%AD%B8%E3%80%91google-drive-api-upload-%E4%BD%BF%E7%94%A8-python-%E4%B8%8A%E5%82%B3%E5%88%B0%E6%8C%87%E5%AE%9A%E8%B3%87%E6%96%99%E5%A4%BE-%E6%95%99%E5%AD%B8/
import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
import os
import io
import time
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload, MediaIoBaseDownload
from httplib2 import Http

SCOPES = ['https://www.googleapis.com/auth/drive']

class My_Google_Drive():
    def update_file(self,service, update_drive_service_name, local_file_path, update_drive_service_folder_id):
        """
        將本地端的檔案傳到雲端上
        :param update_drive_service_folder_id: 判斷是否有 Folder id 沒有的話，會上到雲端的目錄
        :param service: 認證用
        :param update_drive_service_name: 存到 雲端上的名稱
        :param local_file_path: 本地端的位置
        :param local_file_name: 本地端的檔案名稱
        """
        print("正在上傳檔案...")
        if update_drive_service_folder_id is None:
            file_metadata = {'name': update_drive_service_name}
        else:
            # print(update_drive_service_folder_id)
            file_metadata = {'name': update_drive_service_name,
                            'parents': update_drive_service_folder_id}

        media = MediaFileUpload(local_file_path, )
        file_metadata_size = media.size()
        start = time.time()
        file_id = service.files().create(body=file_metadata, media_body=media, fields='id').execute()
        end = time.time()
        print("上傳檔案成功！")
        print('雲端檔案名稱為: ' + str(file_metadata['name']))
        print('雲端檔案ID為: ' + str(file_id['id']))
        print('檔案大小為: ' + str(file_metadata_size) + ' byte')
        print("上傳時間為: " + str(end-start))

        return file_metadata['name'], file_id['id']

    def search_folder(self,service, update_drive_folder_name=None):
        """
        如果雲端資料夾名稱相同，則只會選擇一個資料夾上傳，請勿取名相同名稱
        :param service: 認證用
        :param update_drive_folder_name: 取得指定資料夾的id，沒有的話回傳None，給錯也會回傳None
        :return:
        """
        get_folder_id_list = []
        # print(len(get_folder_id_list))
        if update_drive_folder_name is not None:
            response = service.files().list(fields="nextPageToken, files(id, name)", spaces='drive',
                                        q = "name = '" + update_drive_folder_name + "' and mimeType = 'application/vnd.google-apps.folder' and trashed = false").execute()
            for file in response.get('files', []):
                # Process change
                # print('Found file: %s (%s)' % (file.get('name'), file.get('id')))
                get_folder_id_list.append(file.get('id'))
            if len(get_folder_id_list) == 0:
                print("你給的資料夾名稱沒有在你的雲端上！，因此檔案會上傳至雲端根目錄")
                return None
            else:
                return get_folder_id_list
        return None

    def file_upload(self,is_update_file_function,update_drive_service_name,update_file_path,update_drive_service_folder_name):
        creds = None
        if os.path.exists('token.pickle'):
            with open('token.pickle', 'rb') as token:
                creds = pickle.load(token)
        # If there are no (valid) credentials available, let the user log in.
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    'credentials.json', SCOPES)
                creds = flow.run_local_server(port=0)
            # Save the credentials for the next run
            with open('token.pickle', 'wb') as token:
                pickle.dump(creds, token)

        service = build('drive', 'v3', credentials=creds)

        # print("is_update_file_function")
        # print(type(is_update_file_function))
        # print(is_update_file_function)

        if is_update_file_function is True:
                # print(update_file_path + update_drive_service_name)
                print("=====執行上傳檔案=====")
                # 清空 雲端垃圾桶檔案
                # trashed_file(service=service, is_delete_trashed_file=True)
                get_folder_id = self.search_folder(service = service, update_drive_folder_name = update_drive_service_folder_name)
                # 搜尋要上傳的檔案名稱是否有在雲端上並且刪除
                #search_file(service=service, update_drive_service_name=update_drive_service_name,
                #            is_delete_search_file=True)
                # 檔案上傳到雲端上
                self.update_file(service=service, update_drive_service_name=update_drive_service_name,
                            local_file_path=update_file_path+'/' + update_drive_service_name, update_drive_service_folder_id=get_folder_id)
                print("=====上傳檔案完成=====")

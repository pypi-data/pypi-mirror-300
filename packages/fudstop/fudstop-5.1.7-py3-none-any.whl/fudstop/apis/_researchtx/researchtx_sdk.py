from imps import *

import os
from dotenv import load_dotenv
load_dotenv()
import requests
case_id = os.environ.get('divorce_case_id')


class ResearchTexasSDK:
    def __init__(self):
        pass


    async def get_filings(self,id:str=case_id, page_size:int=50, search_text:str='', headers:str=None):
        """Get case filings"""
        url = f"https://research.txcourts.gov/CourtRecordsSearch/case/{id}/events"
        
        r = requests.post(url=url, data={"pageSize":page_size,"pageIndex":0,"sortNewestToOldest":False,"searchText":search_text,"isSearchAll":True,"eventType":0}, headers=headers)
        print(r)
        if r.status_code == 200:
            r = r.json()
            
            events = r.get('events')

            filingCode = [i.get('filingCode') for i in events]
            description = [i.get('description') for i in events]
            submitted = [i.get('submitted') for i in events]
            submitterFullName = [i.get('submitterFullName') for i in events]
            docketed = [i.get('docketed') for i in events]
            # jurisdiction = [i.get('jurisdiction') for i in events]
            # jurisdictionKey = [i.get('jurisdictionKey') for i in events]
            # externalKey = [i.get('externalKey') for i in events]
            # ofsFilingID = [i.get('ofsFilingID') for i in events]
            # eventType = [i.get('eventType') for i in events]
            # documentIndexNumber = [i.get('documentIndexNumber') for i in events]
            # highlights = [i.get('highlights') for i in events]

            # documents = [i.get('documents') for i in events]

            # flat_docs = [item for sublist in documents for item in sublist]

            # documentID = [i.get('documentID') for i in flat_docs]
            # documentKey = [i.get('documentKey') for i in flat_docs]
            # documentCategoryCode = [i.get('documentCategoryCode') for i in flat_docs]
            # documentSecurityCode = [i.get('documentSecurityCode') for i in flat_docs]
            # fileName = [i.get('fileName') for i in flat_docs]
            # fileSize = [i.get('fileSize') for i in flat_docs]
            # pageCount = [i.get('pageCount') for i in flat_docs]
            # description = [i.get('description') for i in flat_docs]

            # documentStatus = [i.get('documentStatus') for i in flat_docs]

            # externalSource = [i.get('externalSource') for i in flat_docs]
            # externalKey = [i.get('externalKey') for i in flat_docs]
            # jurisdictionKey = [i.get('jurisdictionKey') for i in flat_docs]



            # filingId = [i.get('filingId') for i in flat_docs]
            # isRedactedVersionAvailable = [i.get('isRedactedVersionAvailable') for i in flat_docs]


            data_dict = {
                'filing_code': filingCode,
                'description': description,
                'submitted': submitted,
                'submitter_full_name': submitterFullName,
                'docketed': docketed,

            }
                        # Find the maximum length
            max_length = max(len(lst) for lst in data_dict.values())

            # Ensure all lists are of the same length by padding shorter lists with None
            for key in data_dict:
                if len(data_dict[key]) < max_length:
                    data_dict[key].extend([None] * (max_length - len(data_dict[key])))
            df = pd.DataFrame(data_dict)

            df.to_csv('filings_divorce.csv')


            return df
        

    async def get_events(self, headers):
        payload = {"pageSize":50,"pageIndex":0,"sortNewestToOldest":False,"searchText":None,"isSearchAll":True,"eventType":0}
        url = f"https://research.txcourts.gov/CourtRecordsSearch/case/b04183e55b355b628fa3d90671422f9b/events"

        r = requests.post(url, headers=headers, json=payload).json()
        events = r['events']
        docketed = [i.get('docketed') for i in events]
        submitter = [i.get('submitterFullName') for i in events]
        documents = [i.get('documents') for i in events]

        flat_docs = [item for sublist in documents for item in sublist]

        doc_description = [i.get('description') for i in flat_docs]
  
        doc_category = [i.get('documentCategoryCode') for i in flat_docs]
        filing_code = [i.get('filingCode') for i in flat_docs]
        page_count = [i.get('pageCount') for i in flat_docs]

        text_content = [''.join(i.get('textContent')) for i in flat_docs]
        for i in range(len(text_content)):
            if 'textContent' in text_content[i]:
                text_content[i]['textContent'] = text_content[i]['textContent'].replace('\n', ' ')

        submitter_len = len(submitter)
        description_len = len(doc_description)
        category_len = len(doc_category)
        filing_code_len = len(filing_code)
        pages_len = len(page_count)
        text_content_len = len(text_content)
        docketed_len = len(docketed)

        # Find the minimum length among the lists to ensure all lists match
        min_length = min(submitter_len, description_len, category_len, filing_code_len, pages_len, text_content_len, docketed_len)

        # Truncate all lists to the minimum length if necessary
        submitter = submitter[:min_length]
        doc_description = doc_description[:min_length]
        doc_category = doc_category[:min_length]
        filing_code = filing_code[:min_length]
        page_count = page_count[:min_length]
        text_content = text_content[:min_length]
        docketed = docketed[:min_length]

        # Now create the dictionary
        dict_data = { 
            'submitter': submitter,
            'description': doc_description,
            'document_category': doc_category,
            'filing_code': filing_code,
            'pages': page_count,
            'text_content': text_content
        }

        # Create the DataFrame
        df = pd.DataFrame(dict_data)
        df['docketed'] = docketed

        return df
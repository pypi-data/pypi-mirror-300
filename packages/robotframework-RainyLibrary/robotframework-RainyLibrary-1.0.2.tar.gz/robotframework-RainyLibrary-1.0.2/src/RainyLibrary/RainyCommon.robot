*** Settings ***
Resource        ${CURDIR}/imports.robot

*** Keywords ***
Get thai year
    [Documentation]     Get thai year from current AD year
    ...    \n ``year`` is AD year. ex. 2022 
    [Arguments]  ${year}
    ${year_thai}=   Evaluate   ${year} + 543
    [Return]  ${year_thai}

Get day of week in thai
    [Documentation]     Get day of the week in thai
    ...     \n ``day``  as Sunday will return `อาทิตย์`
    [Arguments]   ${day}
    IF    '${day}' == 'Sunday'
        ${date_thai}  Set variable  อาทิตย์
    ELSE IF    '${day}' == 'Monday'
        ${date_thai}  Set variable  จันทร์
    ELSE IF    '${day}' == 'Tuesday'
        ${date_thai}  Set variable  อังคาร
    ELSE IF    '${day}' == 'Wednesday'
        ${date_thai}  Set variable  พุธ
    ELSE IF    '${day}' == 'Thursday'
        ${date_thai}  Set variable  พฤหัส
    ELSE IF    '${day}' == 'Friday'
        ${date_thai}  Set variable  ศุกร์
    ELSE
        ${date_thai}  Set variable  เสาร์
    END
    [Return]  ${date_thai}

Get os platform
    [Documentation]     Get os platform 
    ...     \n either darwin (Mac) or window
    ${platform}=    Evaluate    platform.system()    platform
    ${system}=      String.Convert to lower case      ${platform}
    [Return]        ${system}

Get current date and short month in thai
    [Documentation]     Get current date and short month in thai
    ...     \n ``return`` example 05 ม.ค. 2565
    ${short_month}    DateUtils.Get current date and short month in thai
    [Return]    ${short_month}


Get normalize path
    [Documentation]     Normalizes the given path.
    ...     \n Collapses redundant separators and up-level references.
    ...     \n Converts `/` to `\` on Windows.
    ...     \n Replaces initial ~ or ~user by that user's home directory. 
    [Arguments]    ${path}
    
    ${NORMAL_PATH}=    OperatingSystem.Normalize path    ${path}
    Log    ${NORMAL_PATH}
    [Return]     ${NORMAL_PATH}

Wait until download is completed
    [Documentation]    Verifies that the directory has one or more folder and it is not a temp file.
                        ...     \n returns path to the file
                        ...     \n `retry`  how many time to loop retry
                        ...     \n `wait_time`  how many second to wait before start another retry
                        ...     \n Current version is able to find new file when folder has more one file
    [Arguments]    ${directory}     ${retry}=5      ${wait_time}=2s

    ${list_of_existing_files}  OperatingSystem.List files in directory    ${directory}
    ${total_number_of_existing_files}    Get length     ${list_of_existing_files}
    ${expected_number_of_file_after_download}    Evaluate   ${total_number_of_existing_files}+1
    ${new_files_name}    Set Variable    ''
    ${is_not_temp_file}  Set Variable    ${FALSE}

    FOR     ${INDEX}    IN RANGE    1   ${retry}
        ${list_of_current_files}=       OperatingSystem.List files in directory    ${directory}
        ${number_of_current_files}    Get length     ${list_of_current_files}
        ${is_contains_new_file}=   Run keyword and return status   BuiltIn.Should be equal    ${number_of_current_files}    ${expected_number_of_file_after_download}    Should be ${expected_number_of_file_after_download} file in the download folder

        IF  '${is_contains_new_file}'=='${TRUE}'
            IF   '${total_number_of_existing_files}'=='0'
                ${new_files_name}   Set Variable    ${list_of_current_files[0]}
            ELSE
                ${new_files_name}   GeneralUtils.check_value_in_file     ${list_of_existing_files}    ${list_of_current_files}
            END
            ${is_not_temp_file}    Run keyword and return status   BuiltIn.Should not match regexp    ${new_files_name}    (?i).*\\.tmp    Chrome is still downloading a file
        ELSE
            ${is_not_temp_file}     Set Variable    ${FALSE}
        END
        ${result}=      Evaluate    ${is_contains_new_file} and ${is_not_temp_file}
        Exit For Loop If    '${result}'=='${TRUE}'
        BuiltIn.Sleep   ${wait_time}
    END
    Should be true  ${result}   msg=not found file in download_directory

    ${file_path}=    OperatingSystem.Join path    ${directory}    ${new_files_name}

    [Return]    ${file_path}

PDF should contain
    [Documentation]     Verify if pdf file contains expected message or not
    [Arguments]  ${pdf_path}     ${message}
    ${path}=    Get normalize path  ${pdf_path}
    ${txt}      Pdf2TextLibrary.Convert Pdf To Txt    ${path}
    Should Contain      ${txt}      ${message}

Write new row to excel file
    [Documentation]     write new row at the end to excel file
    ...     \n ``row_data_as_a_list`` is a list of data represent number of colum in a row ex. ['1','10637','delivered']
    ...     \n ``excel_file_path`` absolute path to write the data into
    [Arguments]     ${row_data_as_a_list}   ${excel_file_path}
    ${date}=	DateTime.Get current date	result_format=epoch     exclude_millis=yes
    ${date}=    Convert to integer  ${date}
    ExcelLibrary.Open excel document    ${excel_file_path}    export_file${date}
    ${info_from_excel}=             ExcelLibrary.Read excel column    ${1}
    ${number_of_row}=               Get length  ${info_from_excel}
    ${row_number_to_write_to}=      Evaluate    ${number_of_row}+1
    ExcelLibrary.Write excel row    row_num=${row_number_to_write_to}   row_data=${row_data_as_a_list}
    ExcelLibrary.Save excel document     filename=${excel_file_path}
    ExcelLibrary.Close all excel documents

Get body and link from email
    [Documentation]     get email body and link from any email providers using imaplibrary.
    ...     \n filter using sender address   
    ...     \n ``timeout`` how long in second you want to wait for the email   
    [Arguments]     ${email}    ${password}     ${sender_address}   ${timeout}=60
    Wait until keyword succeeds    40x    10s
    ...            ImapLibrary2.Open mailbox      host=imap.gmail.com       user=${email}    password=${password}
    ${index}=      ImapLibrary2.Wait for email    sender=${sender_address}  status=UNSEEN    timeout=${timeout}
    ${parts}=      ImapLibrary2.Walk Multipart Email    ${index}
    FOR    ${i}    IN RANGE    ${parts}
        ImapLibrary2.Walk Multipart Email    ${index}
        ${content-type} =    ImapLibrary2.Get Multipart Content Type
        Continue For Loop If    '${content-type}' != 'text/html'
        ${payload} =    ImapLibrary2.Get Multipart Payload    decode=True
        ${link}=        ImapLibrary2.Get Links From Email    ${index}
    END
    ImapLibrary2.Delete All Emails
    ImapLibrary2.Close Mailbox
    ${links}=    GeneralUtils.decode_url   ${link}
    [Return]    ${payload}  ${links}

Get email body
    [Documentation]     get email body from any email providers using imaplibrary.
    ...    \n filter using sender address
    ...    \n ``timeout`` how long in second you want to wait for the email      
    [Arguments]     ${email}    ${password}     ${sender_address}       ${timeout}=60
    ImapLibrary2.Open mailbox      host=imap.gmail.com       user=${email}    password=${password}
    ${index}=           ImapLibrary2.Wait for email    sender=${sender_address}     status=UNSEEN    timeout=${timeout}
    ${text}=            ImapLibrary2.Get Email Body    ${index}
    ${text_replace}=    Replace string      ${text}         \n      ${EMPTY}
    ImapLibrary2.Delete All Emails
    ImapLibrary2.Close Mailbox
    [Return]    ${text_replace}

Column in excel file should contains correct information
    [Documentation]     check if column in excel file contains correct information
    ...     \n reading column of all rows and expected at least 1 to match expected information
    ...     \n ``list_of_expected_information`` is a list contains contain expected information
    ...     \n ``column_to_read`` is an integer indicate column number to read
    [Arguments]     ${excel_file_path}  ${list_of_expected_information}     ${column_to_read}
    ${date}=	Get current date	result_format=epoch     exclude_millis=yes
    ${date}=    Convert to integer  ${date}
    ExcelLibrary.Open excel document    ${excel_file_path}    export_file${date}
    ${info_from_excel}=    ExcelLibrary.Read Excel Column    ${column_to_read}
    Collections.List Should Contain Sub List    ${info_from_excel}  ${list_of_expected_information}
    ExcelLibrary.Close all excel documents

Column in exported excel file should exaclty match
    [Documentation]     check if column in excel file contains correct information
    ...     \n reading column of all rows and expected all to match expected information
    ...     \n ``list_of_expected_information`` is a list contains contain expected information
    ...     \n ``column_to_read`` is an integer indicate column number to read
    [Arguments]     ${excel_file_path}  ${list_of_expected_information}     ${column_to_read}
    ${date}=	Get current date	result_format=epoch     exclude_millis=yes
    ${date}=    Convert to integer  ${date}
    ExcelLibrary.Open excel document    ${excel_file_path}    export_file${date}
    ${info_from_excel}=    ExcelLibrary.Read Excel Column    ${column_to_read}
    Collections.Lists Should Be Equal    ${info_from_excel}  ${list_of_expected_information}
    ExcelLibrary.Close all excel documents

Random thai mobile number
    [Documentation]    Random thai mobile number start with 08
    ${random}        Generate random string    8    0123456789
    ${mobile_number}    Catenate    SEPARATOR=  08  ${random}
    [Return]    ${mobile_number}

Random thai citizen id
    [Documentation]     Random thai citizen id 13 digit
    ${random_1}           Evaluate        random.randrange(1, 9)
    ${random_2}           Evaluate        random.randrange(0, 10)
    ${random_3}           Evaluate        random.randrange(0, 10)
    ${random_4}           Evaluate        random.randrange(0, 10)
    ${random_5}           Evaluate        random.randrange(0, 10)
    ${random_6}           Evaluate        random.randrange(0, 10)
    ${random_7}           Evaluate        random.randrange(0, 10)
    ${random_8}           Evaluate        random.randrange(0, 10)
    ${random_9}           Evaluate        random.randrange(0, 10)
    ${random_10}          Evaluate        random.randrange(0, 10)
    ${random_11}          Evaluate        random.randrange(0, 10)
    ${random_12}          Evaluate        random.randrange(0, 10)
    ${sum}                Evaluate        ${random_1}*13 + ${random_2}*12 + ${random_3}*11 + ${random_4}*10 + ${random_5}*9 + ${random_6}*8 + ${random_7}*7 + ${random_8}*6 + ${random_9}*5 + ${random_10}*4 + ${random_11}*3 + ${random_12}*2
    ${random_13}          Evaluate        ${sum} % 11
    ${mod}                Evaluate        11 - ${random_13}
    IF  '${mod}'=='10'
        ${mod}            Evaluate        0
    ELSE IF  '${mod}'=='11'
        ${mod}            Evaluate        1
    END
    ${citizen_id}         Evaluate        ('${random_1}' + '${random_2}' + '${random_3}' + '${random_4}' + '${random_5}' + '${random_6}' + '${random_7}' + '${random_8}' + '${random_9}' + '${random_10}' + '${random_11}' + '${random_12}' + '${mod}')
    [Return]            ${citizen_id}

Get number of days in month
    [Documentation]     Get number of days in month
    ...     \n `month` is the month number you wish to get days (1-12), default as now
    ...     \n `year` is the year you wish to get days (AD, 2022,2023), default as now
    [Arguments]     ${month}=${NONE}        ${year}=${NONE}     

    ${number_of_days_in_month}=     DateUtils.Get number of days in month   ${month}    ${year}
    [Return]    ${number_of_days_in_month}

Get days remaining in current month
    [Documentation]     Get days remaining in current month

    ${number_of_days_left_in_month}=     DateUtils.Get days remaining in current month
    [Return]    ${number_of_days_left_in_month}
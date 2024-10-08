*** Settings ***
Resource        ${CURDIR}/imports.robot

*** Keywords ***
Click element when ready
    [Documentation]     Keyword to wait for element to be visible before clicking.
    ...     \n default retry clicking is 3 times
    ...     \n can also wait for only page is CONTAINS element instead of visible
    [Arguments]     ${locator}  ${retry}=4      ${only_contains}=${FALSE}       ${timeout}=${GLOBAL_TIMEOUT}

    FOR     ${i}    IN RANGE    1   ${retry}
        IF  ${only_contains}
            ${wait_status}=             Run keyword and ignore error   SeleniumLibrary.Wait until page contains element     ${locator}    ${timeout}
            ${err_msg_wait}=            Convert to string       ${wait_status[1]}
            ${is_not_stale_wait}=       Run keyword and return status    Should not contain     ${err_msg_wait}      StaleElementReferenceException
        ELSE
            SeleniumLibrary.Wait until element is enabled    ${locator}     ${timeout}
            ${wait_status}=             Run keyword and ignore error   SeleniumLibrary.Wait until element is visible        ${locator}   ${timeout}
            ${err_msg_wait}=            Convert to string       ${wait_status[1]}
            ${is_not_stale_wait}=       Run keyword and return status    Should not contain     ${err_msg_wait}      StaleElementReferenceException
        END
        ${is_success}=          Run keyword and ignore error   SeleniumLibrary.Click element   ${locator}
        ${err_msg}=             Convert To String       ${is_success[1]}
        ${is_obsecure}=         Run keyword and return status    Should not contain     ${err_msg}       Other element would receive the click
        ${is_not_stale}=        Run keyword and return status    Should not contain     ${err_msg}       StaleElementReferenceException
        ${is_no_err}=           Run keyword and return status    Should be true        '${err_msg}' == '${NONE}'
        ${is_empty_wait}=       Run keyword and return status    Should be true         '${err_msg_wait}' == '${NONE}'
        ${result}=              Evaluate    ${is_success} and ${is_not_stale_wait} and ${is_obsecure} and ${is_not_stale} and ${is_no_err} and ${is_empty_wait}
        Exit for loop if        ${result}
        Log     'retry clicking element for ${i} time with error: ${err_msg}, ${err_msg_wait}'   level=WARN
    END
    Should be true  ${result}   msg="Failed to click element after ${retry} retry"

Default test teardown
    [Documentation]    Capture screenshot for every test case 
    ...     \n all failed case always logs and returns the HTML source of the current page or frame.
    Run Keyword And Ignore Error    SeleniumLibrary.Capture Page Screenshot
    Run Keyword If Test Failed      Run Keyword And Ignore Error    SeleniumLibrary.Log Source
    SeleniumLibrary.Close all browsers

Open chrome browser
    [Documentation]     Open chrome browser with so many option to customize.
                        ...     \n ``browser_mode`` can be either desktop or mobile to open in mobile resolution
                        ...     \n ``headless`` to open browser in headful or headless mode
                        ...     \n ``extension_full_path`` if not empty will install chrome extention from given path 
                        ...     \n ``with_download_dir`` create chrome driver with download directory default at ${OUTPUT_DIR}/downloads_${current_time_epoch_format}
                        ...     \n ``with_proxy`` create chrome driver and start local proxy for capturing network 
                        ...     \n ``path_to_browsermob_proxy`` path to browsermob installation file
                        ...     \n ``with_save_pdf`` True if want to automatically save PDF from chorme preview printing screen
    [Arguments]     ${url}    
                    ...     ${browser_mode}=desktop
                    ...     ${headless}=${FALSE}
                    ...     ${extension_full_path}=${EMPTY}
                    ...     ${with_download_dir}=${FALSE}
                    ...     ${with_proxy}=${FALSE}
                    ...     ${path_to_browsermob_proxy}=${EMPTY}
                    ...     ${with_save_pdf}=${FALSE}

    ${chrome_options}=     Evaluate       sys.modules['selenium.webdriver'].ChromeOptions()     sys, selenium.webdriver
    Call Method     ${chrome_options}     add_argument     --disable-infobars
    Call Method     ${chrome_options}     add_argument     --window-size\=1920,1080
    Call Method     ${chrome_options}     add_argument     --disable-dev-shm-usage
    Call Method     ${chrome_options}     add_argument     --disable-gpu
    Call Method     ${chrome_options}     add_argument     --no-sandbox
    Call Method     ${chrome_options}     add_argument     --ignore-certificate-errors

    IF  '${extension_full_path}' != '${EMPTY}'
            Call Method     ${chrome_options}      add_extension   ${extension_full_path}
    END

    IF  ${headless}
        Call Method     ${chrome_options}      add_argument    --headless
        Call Method     ${chrome_options}      add_argument    --window-size\=1920,1080
    END

    IF  ${with_download_dir}
        ${current_time}=            BuiltIn.Get time    epoch
        ${download_directory}=      OperatingSystem.Join path    ${OUTPUT_DIR}    downloads_${current_time}
        OperatingSystem.Create directory            ${download_directory}
        Wait until keyword succeeds    5x    2s     OperatingSystem.Directory Should Exist  ${download_directory}
        ${prefs}=                   BuiltIn.Create dictionary    download.default_directory=${download_directory}
        Log to console      file will be downloaded to ${download_directory}
        BuiltIn.Call Method    ${chrome_options}    add_experimental_option    prefs    ${prefs}
    ELSE
        ${download_directory}=  Set variable    ${EMPTY}
    END

    IF  ${with_proxy}
        ${random_proxy_port}=   Evaluate    random.sample(range(30000, 45000), 1)    random
        &{proxt_port}=          Create Dictionary   port=${random_proxy_port}[0]
        BrowserMobProxyLibrary.Start Local Server      ${path_to_browsermob_proxy}
        BrowserMobProxyLibrary.Create Proxy    ${proxt_port}
        Call Method    ${chrome_options}    add_argument      --proxy-server\=127.0.0.1:${random_proxy_port}[0]
        Call Method    ${chrome_options}    add_argument      ignore-certificate-errors
    END
    
    IF  ${with_save_pdf}
        ${current_time}=            BuiltIn.Get time    epoch
        ${download_directory}=      OperatingSystem.Join path    ${OUTPUT_DIR}    downloads_${current_time}
        OperatingSystem.Create directory            ${download_directory}
        Wait until keyword succeeds    5x    2s     OperatingSystem.Directory Should Exist  ${download_directory}
        ${json}=        JSONLibrary.Convert String to JSON    { "appState": { "recentDestinations": [{"id": "Save as PDF","origin": "local","account":""}],"selectedDestinationId": "Save as PDF","version": ${2}}}
        ${prefs}=       Create Dictionary    
                        ...     savefile.default_directory=${download_directory}
                        ...     download.default_directory=${download_directory}
                        ...     download.prompt_for_download=${FALSE}
                        ...     directory_upgrade=${TRUE}   
                        ...     plugins.plugins_disabled=Chrome PDF Viewer
                        ...     printing.print_preview_sticky_settings=${json}
                        ...     plugins.always_open_pdf_externally=${TRUE}
                        ...     download.extensions_to_open=applications/pdf
        Call Method     ${chrome_options}     add_argument     --kiosk-printing
        Call Method     ${chrome_options}     add_argument     --disable-print-preview
        Call Method     ${chrome_options}     add_experimental_option    prefs    ${prefs}
    END

    IF  '${browser_mode}' == 'mobile'
        ${mobile_emulation}=    Create Dictionary    deviceName=iPhone X
        Call Method    ${chrome_options}    add_experimental_option    mobileEmulation    ${mobile_emulation}
    END

    SeleniumLibrary.Create WebDriver    Chrome      chrome_options=${chrome_options}
    SeleniumLibrary.Go To     ${url}

    IF  '${browser_mode}' == 'desktop'
        SeleniumLibrary.Maximize Browser Window
    END

    [Return]    ${download_directory}

Input text to element when ready
    [Documentation]     Wait for element to be visible first before input text. Retry 4 times
    [Arguments]     ${locator}     ${text}     ${clear}=${TRUE}     ${timeout}=${GLOBAL_TIMEOUT}
    SeleniumLibrary.Wait until element is visible    ${locator}     ${timeout}
    SeleniumLibrary.Wait until element is enabled    ${locator}     ${timeout}
    FOR    ${index}    IN RANGE    1    4
        ${result_msg}=      Run Keyword And Ignore Error    SeleniumLibrary.Input Text      ${locator}     ${text}     clear=${clear}
        ${err_msg}=         Convert To String       ${result_msg[1]}
        ${is_success}=                  Run Keyword And Return Status    Should Be Equal        ${err_msg}      None
        ${is_not_loading_error}=        Run Keyword And Return Status    Should Not Contain     ${err_msg}      invalid element state
        Exit For Loop If        ${is_success} or ${is_not_loading_error}
    END
    Should Be True      ${is_success}   msg=Unable to input text to element after 4 retry

Select option by label when ready
    [Documentation]     Wait until element is visible first before select from list by label
    [Arguments]     ${locator}     ${label}     ${timeout}=${GLOBAL_TIMEOUT}
    SeleniumLibrary.Wait until element is visible    ${locator}     ${timeout}
    FOR    ${index}    IN RANGE    1    10
        ${result_msg}=      Run Keyword And Ignore Error    Select From List By Label      ${locator}     ${label}
        ${err_msg}=         Convert To String       ${result_msg[1]}
        ${is_success}=                  Run Keyword And Return Status    Should Be Equal        ${err_msg}      None
        ${is_not_loading_error}=        Run Keyword And Return Status    Should Not Contain     ${err_msg}      invalid element state
        Exit For Loop If        ${is_success} or ${is_not_loading_error}
    END
    Should Be True      ${is_success}   msg=Unable to select option dropdownlist after 10 retry


Get text from element when ready
    [Documentation]     Wait until element is visible first before get text from element. 
                        ...     \n default timeout is same as ${GLOBAL_TIMEOUT}
    [Arguments]     ${locator}      ${timeout}=${GLOBAL_TIMEOUT}
    SeleniumLibrary.Wait until element is visible    ${locator}     ${timeout}
    ${text}=    SeleniumLibrary.Get text    ${locator}
    [Return]    ${text}

Get element count when ready
    [Documentation]     Wait until element is visible first before get element count
                        ...     \n default timeout is same as ${GLOBAL_TIMEOUT}
    [Arguments]     ${locator}   ${timeout}=${GLOBAL_TIMEOUT}
    SeleniumLibrary.Wait until element is visible       ${locator}      ${timeout}
    ${count}=   SeleniumLibrary.Get Element Count       ${locator}
    [Return]    ${count}

Get element attribute when ready
    [Documentation]     Wait until element is visible first before get element attribute
    ...     \n default timeout is same as ${GLOBAL_TIMEOUT}
    [Arguments]     ${locator}      ${attribute}    ${only_contain}=${FALSE}    ${timeout}=${GLOBAL_TIMEOUT}
    IF  ${only_contain}
        Wait until keyword succeeds    5x    2s     SeleniumLibrary.Wait until page contains element    ${locator}      ${timeout}
    ELSE IF     ${only_contain} == ${FALSE}
        Wait until keyword succeeds    5x    2s     SeleniumLibrary.Wait until element is visible       ${locator}      ${timeout}
    END
    ${att}=   SeleniumLibrary.Get element attribute     ${locator}  ${attribute}
    [Return]    ${att}

Scroll element into view when ready
    [Documentation]     Wait until page contains element then scroll the element into view
    ...     \n default timeout is same as ${GLOBAL_TIMEOUT}
    [Arguments]     ${locator}      ${retry}=4      ${timeout}=${GLOBAL_TIMEOUT}
    FOR     ${i}    IN RANGE   0    ${retry}
        SeleniumLibrary.Wait until page contains element    ${locator}      ${timeout}
        SeleniumLibrary.Scroll element into view            ${locator}
        ${is_visible}=  Run keyword and return status   SeleniumLibrary.Wait until element is visible       ${locator}      ${timeout}
        Exit for loop if    ${is_visible}
    END

Browse file when ready
    [Documentation]     Wait until page contains element then choose file from file path
    ...     \n default timeout is same as ${GLOBAL_TIMEOUT}
    [Arguments]     ${locator}      ${file_path}    ${timeout}=${GLOBAL_TIMEOUT}
    SeleniumLibrary.Wait until Page contains element   ${locator}       ${timeout}
    SeleniumLibrary.Choose File     ${locator}  ${file_path}


Get value from element when ready
    [Documentation]    Wait until element is visible first before get element attribute value
    ...     \n default timeout is same as ${GLOBAL_TIMEOUT}
    [Arguments]     ${locator}  ${only_contain}=${FALSE}    ${timeout}=${GLOBAL_TIMEOUT}
    IF  ${only_contain}
        SeleniumLibrary.Wait until page contains element    ${locator}      ${timeout}
    ELSE IF     ${only_contain} == ${FALSE}
        SeleniumLibrary.Wait until element is visible       ${locator}      ${timeout}
    END
    ${value}=   SeleniumLibrary.Get value     ${locator}
    [Return]    ${value}


Manually clear input from textbox
    [Documentation]  sometime selenium cannot clear text box easily
    ...     \n this keyword will get length of text in text box then press BACKSPACE key n number
    ...     \n equal to that amount     
    [Arguments]     ${locator}      ${timeout}=${GLOBAL_TIMEOUT}
    ${current_value}=   RainyWebCommon.Get value from element when ready    ${locator}      ${timeout}
    ${word_length}=     Get length      ${current_value}
    FOR     ${i}    IN RANGE   ${word_length}
        Press keys     ${locator}       BACKSPACE
    END

Scroll to top of page using java script
    [Documentation]  Scroll to top of page using java script
    Execute javascript          window.scrollTo(0,0)

Scroll to bottom of page using java script
    [Documentation]  Scroll to bottom of page using java script
    ${w}    ${h}        Get Window Size
    ${bottom}           Evaluate    ${h}+10000
    Execute javascript          window.scrollTo(0,${bottom})


Wait until element is visible except stale
    [Documentation]  Wait until element is visible except stale
    ...     \n default timeout is same as ${GLOBAL_TIMEOUT}
    [Arguments]    ${locator}       ${timeout}=${GLOBAL_TIMEOUT}
    FOR     ${i}    IN RANGE    1       15
        ${status}           Run keyword and ignore error   SeleniumLibrary.Wait until element is visible    ${locator}      ${timeout}
        ${err_msg}=         Convert To String       ${status[1]}
        ${is_not_stale}=    Run keyword and return status    Should not contain     ${err_msg}      StaleElementReferenceException
        Exit For Loop If        ${is_not_stale}
    END
    SeleniumLibrary.Wait until element is visible    ${locator}      ${timeout}
    BuiltIn.Should Be True  ${is_not_stale}     msg='element is not visible and still in stale stage'


Click element at coordinates when ready
    [Documentation]     Keyword to wait for element to be visible before clicking.
    ...     \n default retry clicking is 3 times
    ...     \n can also wait for only page is CONTAINS element instead of visible
    ...     \n log as warning if retry more than 1, in case it's actually a bug
    ...     \n default timeout is same as ${GLOBAL_TIMEOUT}
    [Arguments]     ${locator}      ${xoffset}  ${yoffset}      ${retry}=4      ${only_contains}=${FALSE}       ${timeout}=${GLOBAL_TIMEOUT}
    
    FOR     ${i}    IN RANGE    1   ${retry}
        IF  ${only_contains}
            SeleniumLibrary.Wait until page contains element   ${locator}       ${timeout}
        ELSE
            SeleniumLibrary.Wait until element is visible   ${locator}      ${timeout}
        END
        ${is_success}=          Run keyword and ignore error   SeleniumLibrary.Click element at coordinates    ${locator}     ${xoffset}  ${yoffset}  
        ${err_msg}=             Convert To String       ${is_success[1]}
        ${is_obsecure}=         Run keyword and return status    Should not contain     ${err_msg}       Other element would receive the click
        ${is_not_stale}=        Run keyword and return status    Should not contain     ${err_msg}       element is not attached to the page document
        ${is_no_err}=           Run keyword and return status    Should be true        '${err_msg}' == '${NONE}'
        ${result}=              Evaluate    ${is_success} and ${is_obsecure} and ${is_obsecure} and ${is_not_stale} and ${is_no_err}
        Exit for loop if        ${result}
        Log     'retry clicking element for ${i} time with error: ${err_msg}'   level=WARN
    END
    Should be true  ${result}   msg="Failed to click element after ${retry} retry"


Click image on screen 
    [Documentation]  Clicking on image using xy coordinates
    ...     \n keyword will try to find image on the screen from expected image first 
    ...     \n then will try to click it using x,y coordinates at the middle of the image
    ...     \n default threshold to compare is 0.8 = 80%
    ...     \n ``abs_expected_image_path`` is the absolute path of expected image to be clicked
    [Arguments]     ${abs_expected_image_path}      ${threshold}=0.8    ${timeout}=${GLOBAL_TIMEOUT}
    ${is_found_image}   ${xy}=  RainyWebCommon.Image should be visible on screen   ${expected_image}   ${threshold}=0.8
    
    IF      ${is_found_image}
        RainyWebCommon.Click element at coordinates when ready      body    ${xy[0]}     ${xy[1]}   ${timeout}
    ELSE
        Should be true  ${is_found_image}   msg="Image was not found on the screen"
    END

Close all browsers and stop proxy server
    [Documentation]  Closing all browser and stop browermob proxy 
    SeleniumLibrary.Close All Browsers
    Run Keyword And Ignore Error    BrowserMobProxyLibrary.Stop Local Server

Start capture network traffic
    [Documentation]  Start capturing network traffic 
    ...    \n ``traffic_id`` is the id ref to network traffic
    [Arguments]     ${traffic_id}
    &{capture_option}=    Create Dictionary   captureHeaders=true         captureContent=true
    BrowserMobProxyLibrary.New Har     ${traffic_id}   options=${capture_option}

Stop capture network traffic
    [Documentation]     stop capturing network traffic for browsermob proxy
    ...    \n ``quiet_period` number of miliseconds the network needs to be quiet for
    ...    \n ``timeout`` max number of miliseconds to wait
    ...    \n ``return`` network traffic as json file 
    [Arguments]     ${quiet_period}=3000    ${timeout}=10000
    BrowserMobProxyLibrary.Wait For Traffic To Stop    3000  10000
    ${result_har_json}=    BrowserMobProxyLibrary.Get Har As JSON
    ${network_traffic}=    JSONLibrary.Convert String to JSON   ${result_har_json}
    [Return]    ${network_traffic}

Get WebElement when ready
    [Documentation]     Returns the first WebElement matching the given locator when ready
    [Arguments]     ${locator}      ${timeout}=${GLOBAL_TIMEOUT}
    SeleniumLibrary.Wait until element is visible    ${locator}     ${timeout}
    ${element}=     SeleniumLibrary.Get WebElement      ${locator}
    [Return]    ${element}

Get WebElements when ready
    [Documentation]     Returns a list of WebElement objects matching the locator when ready
    [Arguments]     ${locator}      ${timeout}=${GLOBAL_TIMEOUT}
    SeleniumLibrary.Wait until element is visible    ${locator}     ${timeout}
    ${elements}=     SeleniumLibrary.Get WebElements      ${locator}
    [Return]    ${elements}

Mouse over when ready
    [Documentation]     Simulates hovering the mouse over the element locator when ready
    [Arguments]     ${locator}
    SeleniumLibrary.Wait until element is visible       ${locator}
    SeleniumLibrary.Mouse over      ${locator}

Verify element text when ready
    [Documentation]     Verifies that element locator contains exact the text expected when ready 
    ...    \n if you want to match the exact text, not a substring
    [Arguments]     ${locator}      ${expected}     ${override_error_msg}=${None}    ${ignore_case}=${False}       ${timeout}=${GLOBAL_TIMEOUT}
    SeleniumLibrary.Wait until element is visible       ${locator}      ${timeout}
    SeleniumLibrary.Element text should be      ${locator}      ${expected}     ${override_error_msg}    ${ignore_case}

Verify element should contains text when ready
    [Documentation]     Verifies that element locator contains text expected when ready if a substring match is desired
    [Arguments]     ${locator}      ${expected}     ${override_error_msg}=${None}    ${ignore_case}=${False}       ${timeout}=${GLOBAL_TIMEOUT}
    SeleniumLibrary.Wait until element is visible       ${locator}      ${timeout}
    SeleniumLibrary.Element should contain      ${locator}      ${expected}     ${override_error_msg}    ${ignore_case}

Open and switch to new tab 
    [Documentation]     Open a new tab in the same browser session and switch to it
    ...     \n accept url if you want to open a newtab to a url. default is blank.
    [Arguments]     ${url}=${EMPTY}
    Execute Javascript    window.open('${url}');
    ${headles}    SeleniumLibrary.Get window handles
    SeleniumLibrary.Switch Window    ${headles}[1]


Image should be visible on screen   
    [Documentation]     Find image on current screen by comparing screenshot of current screen and expected image 
    ...     \n default threshold is 0.8 meaning 80% of 2 images should match 
    ...     \n Return true/false and xy of the expected image on screen if any
    ...     \n ``abs_expected_image_path`` is the absolute path of expected image 
    [Arguments]     ${abs_expected_image_path}   ${threshold}=0.8
    ${current_time}=            BuiltIn.Get time    epoch
    ${screen_screenshot}=       SeleniumLibrary.Capture Page Screenshot     ${OUTPUT_DIR}${/}screen_screenshot_${current_time}.png
    ${is_found_image}   ${xy}=  ImageUtils.Image should be visible on screen
                                ...     ${abs_expected_image_path}
                                ...     ${screen_screenshot}
                                ...     ${threshold}
    [Return]    ${is_found_image}   ${xy}

Clear text by press key
    [Arguments]    ${locator}
    [Documentation]    Clear all text in text box both of system mac or window
    ${system}=    BuiltIn.Evaluate   platform.system()    platform
    IF  '${system}' == 'Darwin'
        SeleniumLibrary.Press keys   ${locator}   COMMAND+a   BACKSPACE
    ELSE
        SeleniumLibrary.Press keys   ${locator}   CTRL+a   BACKSPACE
    END

Scroll to element
    [Documentation]    Scroll to element using javascript function 'scrollIntoView'
    ...                ${block} defines of vertical align (start, end, center, nearest)
    ...                Make sure that ${GLOBALTIMEOUT} can be accessed globally
    [Arguments]    ${locator}    ${block}=center    ${timeout}=${GLOBAL_TIMEOUT}
    SeleniumLibrary.Wait until page contains element    ${locator}    ${timeout}
    ${elem}=    SeleniumLibrary.Get Webelements    ${locator}
    ${s2l}=    BuiltIn.Get library instance    SeleniumLibrary
    ${driver}=     BuiltIn.Evaluate    $s2l._current_browser() if "_current_browser" in dir($s2l) else $s2l._drivers.current
    BuiltIn.Call Method    ${driver}    execute_script    arguments[0].scrollIntoView({block: "${block}"});    ${elem}[0]
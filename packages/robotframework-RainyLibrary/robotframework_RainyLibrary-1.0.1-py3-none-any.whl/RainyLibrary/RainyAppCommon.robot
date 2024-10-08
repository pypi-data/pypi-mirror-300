*** Settings ***
Resource        ${CURDIR}/imports.robot

*** Keywords ***
Init mobile farm configuration
    [Documentation]  Init rainy mobile farm, Use hand in hand with woody mobile farm management
    ...     \n following global variable will be set
    ...     deviceName,systemPort,udid,remoteUrl,platformVersion
    ...     you can use it in your open application kw

    ${pool_to_use}              Evaluate        ${PABOTEXECUTIONPOOLID}
    ${delay_time}               Evaluate    ${pool_to_use}*5
    Sleep                       ${delay_time}s
    ${valuesetname}=            Acquire value set  set${pool_to_use}
    ${rainyAppiumPort}=        Get value from set     appium_port
    ${rainySystemPort}=        Get value from set     system_port
    ${rainyDeviceName}=        Get value from set     device_info
    ${rainyEmulatorName}=      Get value from set     emulator_name
    ${platformVersion}=         Get value from set     version
    ${url}=                     Get value from set     remote_url
    ${rainySystemPort_int}=    Convert to integer     ${rainySystemPort}
    Set global variable     ${deviceName}           ${rainyDeviceName}
    Set global variable     ${systemPort}           ${rainySystemPort_int}
    Set global variable     ${udid}                 ${rainyEmulatorName}
    Set global variable     ${remoteUrl}            http://${url}:${rainyAppiumPort}/wd/hub
    Set global variable     ${platformVersion}       ${platformVersion}
    Release Value Set


Set resolution
    [Documentation]     Set device resolution according to scroll element size
    [Arguments]       ${scroll_element}     ${percent}=0.3
    RainyAppCommon.Wait until element is visible except stale    ${scroll_element}
    ${getsize} =   AppiumLibrary.Get element size     ${scroll_element}
    ${getcoor} =   AppiumLibrary.Get element location     ${scroll_element}
    ${center_x}    Evaluate    ${getcoor['x']}+${getsize['width']}/2
    ${center_y}    Evaluate    ${getcoor['y']}+${getsize['height']}/2
    ${sideways_center_point}     Evaluate    ${getsize['width']}/2
    ${newY}        Evaluate    ${center_y}-${center_y}*${percent}
    ${bottomY}     Evaluate    ${center_y}-${newY}
    ${newx}        Evaluate    ${center_x}-${center_x}*${percent}
    Set test variable    ${center_x}
    Set test variable    ${center_y}
    Set test variable    ${newY}
    Set test variable    ${bottomY}
    Set test variable    ${newx}

Clear text when ready
    [Documentation]     Keyword to wait for element to be visible before clear text.
    [Arguments]     ${locator}      ${timeout}=${GLOBAL_TIMEOUT}
    RainyAppCommon.Wait until element is visible except stale       ${locator}    ${timeout}
    AppiumLibrary.Clear text                          ${locator}

Tap element when ready
    [Documentation]     There are 2 modes; the first one is to wait until element is ready then tap (this is a default).
    ...    \n another one is to just tap right away and retry if it fails. it will also wait element to be ready before do next taps.
    ...    \n The default for retrying is 3 times.
    ...    \n locator - the locator of element to be tapped
    ...    \n only_contain - this flag indicates whether it will wait until page of element or element is visible, Default is True
    ...    \n timeout - the maximum period of time to wait until page/element is visible, Default timeout is same as ${GLOBAL_TIMEOUT}
    ...    \n wait_until_ready - this flag indicates whether it will wait until element is ready or just do the first tap immediately, Default is True
    ...    \n max_attempts - the number of retrying attempts

    [Arguments]     ${locator}      ${only_contain}=${FALSE}    ${timeout}=${GLOBAL_TIMEOUT}    ${wait_until_ready}=${TRUE}    ${max_attempts}=4
    FOR     ${i}    IN RANGE    1   ${max_attempts}
        IF    ${wait_until_ready} 
            IF  ${only_contain}
                ${wait_status}=    Run keyword and ignore error    RainyAppCommon.Wait until page contain element except stale     ${locator}    ${timeout}
                ${err_msg_wait}=            Convert to string       ${wait_status[1]}
            ELSE
                ${wait_status}=    Run keyword and ignore error    RainyAppCommon.Wait until element is visible except stale    ${locator}   ${timeout}
                ${err_msg_wait}=            Convert to string       ${wait_status[1]}
            END
        ELSE
            ${err_msg_wait}=    Set variable    ${EMPTY}
        END

        ${tap_status}=              Run keyword and ignore error   AppiumLibrary.Tap         ${locator}
        ${err_msg_tap}=             Convert to string       ${tap_status[1]}
        ${result}=                  Evaluate    '${tap_status[0]}' == 'PASS'
        Exit for loop if            ${result}
        # if wait until ready is false it need to set to true for make next loop wait
        ${wait_until_ready}=        Set variable    ${TRUE}
    END
    Should Be True   ${result}    msg='Unable to tap after ${${max_attempts}-1} attempts, with error ${err_msg_tap}, ${err_msg_wait},'

Long press when ready
    [Documentation]     Keyword to wait for element to be visible before long press
    ...    \n default timeout is same as ${GLOBAL_TIMEOUT}
    [Arguments]     ${locator}      ${duration}=1000    ${timeout}=${GLOBAL_TIMEOUT}
    RainyAppCommon.Wait until element is visible except stale     ${locator}    ${timeout}
    AppiumLibrary.Long press         ${locator}       duration=${duration}

Input text to element when ready
    [Documentation]     There are 2 modes; the first one is to wait until element is ready then tap (this is a default).
    ...    \n another one is to just tap right away and retry if it fails. it will also wait element to be ready before do next taps.
    ...    \n The default for retrying is 3 times.
    ...    \n locator - the locator of element to be input
    ...    \n text - that should be input into the element
    ...    \n clear - this flag indicates whether text should be clear or not. Default is True
    ...    \n timeout - the maximum period of time to wait until page/element is visible, Default timeout is same as ${GLOBAL_TIMEOUT}
    ...    \n wait_until_ready - this flag indicates whether it will wait until element is ready or just do the first tap immediately, Default is True
    ...    \n max_attempts - the number of retrying attempts

    [Arguments]     ${locator}      ${text}    ${clear}=${TRUE}     ${timeout}=${GLOBAL_TIMEOUT}    ${wait_until_ready}=${TRUE}    ${max_attempts}=4
    RainyAppCommon.Tap element when ready   ${locator}     timeout=${timeout}    wait_until_ready=${wait_until_ready}    max_attempts=${max_attempts}
    IF  ${clear}
        AppiumLibrary.Clear text      ${locator}
    END
    AppiumLibrary.Input text      ${locator}          ${text}

Hide keyboard until success
    [Documentation]     Try to hide keyboard until it's not shown. retry 10 times
    FOR     ${i}    IN RANGE    1   5
        AppiumLibrary.Hide keyboard
        ${is_shown}=    AppiumLibrary.Is Keyboard Shown
        Exit for loop if    '${is_shown}' == 'False'
    END
    Should be true  ${is_shown}     msg='Keyboard is still shown after 10 retry'

Get text from element when ready
    [Documentation]     Wait until element is visible then get text
    ...    \n default timeout is same as ${GLOBAL_TIMEOUT}
    [Arguments]     ${locator}      ${timeout}=${GLOBAL_TIMEOUT}
    RainyAppCommon.Wait until element is visible except stale   ${locator}    ${timeout}
    ${text}=    AppiumLibrary.Get text    ${locator}
    [Return]    ${text}

Swipe up
    [Documentation]     Swiping up by percent
    ...     \n ``start_x`` starting at 50% of width of the screen
    ...     \n ``start_y`` starting at 80% of hight of the screen, button of the screen
    ...     \n ``end_x``   ending at 50% of width of the screen, same horizontally as start
    ...     \n ``end_y``   ending at 20% of hight of the screen, moving up 
    [Arguments]         ${start_x}=50
                ...     ${start_y}=80
                ...     ${end_x}=50
                ...     ${end_y}=20
                ...     ${duration}=1000
    AppiumLibrary.Swipe by percent    ${start_x}  ${start_y}  ${end_x}  ${end_y}    duration=${duration}

Swipe down
    [Documentation]     Swiping down by percent
    ...     \n ``start_x`` starting at 50% of width of the screen
    ...     \n ``start_y`` starting at 20% of hight of the screen, top of the screen
    ...     \n ``end_x``   ending at 50% of width of the screen, same horizontally as start
    ...     \n ``end_y``   ending at 80% of hight of the screen, moving down 
    [Arguments]         ${start_x}=50
                ...     ${start_y}=20
                ...     ${end_x}=50
                ...     ${end_y}=80
                ...     ${duration}=1000
    AppiumLibrary.Swipe by percent    ${start_x}  ${start_y}  ${end_x}  ${end_y}    duration=${duration}

Move to
    [Documentation]  Move to used this keyword with set resolution
    [Arguments]    ${moveto}
    IF  "${moveto}"=="Left"
        Swipe    ${center_x}        ${center_y}    ${newx}          ${center_y}         1500
    ELSE IF     "${moveto}"=="Right"
        Swipe    ${newx}            ${center_y}    ${center_x}       ${center_y}        1500
    ELSE IF     "${moveto}"=="Top"
        Swipe    ${center_x}        ${center_y}    ${center_x}       ${newY}            2500
    ELSE IF     "${moveto}"=="Bottom"
        Swipe    ${center_x}        ${newY}        ${center_x}       ${center_y}        2500
    END

Find element
    [Documentation]     Find element by swiping down
    [Arguments]         ${target_element}
                ...     ${scroll_panel}
                ...     ${default_scroll_view}=${NONE}
                ...     ${moveto}=Top
                ...     ${percent}=0.3
                ...     ${number_of_scroll}=10
                ...     ${timeout}=${GLOBAL_TIMEOUT}
    ${element_status}=      Run keyword and return status    RainyAppCommon.Wait until element is visible except stale      ${target_element}      ${timeout}
    IF  '${element_status}'=='False'
        Set resolution      ${scroll_panel}    ${percent}
        FOR    ${i}    IN RANGE    ${number_of_scroll}
            Move to    ${moveto}
            ${element_status}=      Run keyword and return status    RainyAppCommon.Wait until element is visible except stale      ${target_element}      ${timeout}
            Exit for loop if    ${element_status}
        END
        Should be true      ${element_status}   msg='Element is not visible after ${number_of_scroll} scroll'
    END
    Should be true      ${element_status}


Wait until element is visible except stale
    [Documentation]         Wait until element is visible except stale
    [Arguments]    ${locator}        ${timeout}=${GLOBAL_TIMEOUT}    ${max_attempts}=5
    FOR     ${i}    IN RANGE    1       ${max_attempts}
        ${is_visible}       Run keyword and ignore error    AppiumLibrary.Wait until element is visible       ${locator}         ${timeout}
        ${err_msg}=         Convert to string       ${is_visible[1]}
        ${is_not_stale}=    Run keyword and return status    Should not contain    ${err_msg}      StaleElementReferenceException
        ${no_err_msg}       Run keyword and return status    Should be equal       ${is_visible[0]}      PASS       msg=${err_msg}
        ${result}=          Evaluate    ${is_not_stale} and ${no_err_msg}
        Exit for loop if        ${result}
    END
    Should be true      ${result}       msg="element either in stale mode or not visible, error message is ${err_msg}"

Wait until page contain element except stale
    [Documentation]         Wait until page contain element except stale
    [Arguments]    ${locator}        ${timeout}=${GLOBAL_TIMEOUT}    ${max_attempts}=5
    FOR     ${i}    IN RANGE    1       ${max_attempts}
        ${is_visible}       Run keyword and ignore error    AppiumLibrary.Wait until page contains element       ${locator}         ${timeout}
        ${err_msg}=         Convert to string       ${is_visible[1]}
        ${is_not_stale}=    Run keyword and return status    Should not contain    ${err_msg}      StaleElementReferenceException
        ${no_err_msg}       Run keyword and return status    Should be equal       ${is_visible[0]}      PASS       msg=${err_msg}
        ${result}=          Evaluate    ${is_not_stale} and ${no_err_msg}
        Exit for loop if        ${result}
    END
    Should be true      ${result}       msg="page either in stale mode or not visible, error message is ${err_msg}"

Click image on screen 
    [Documentation]  Clicking on image using xy coordinates
                    ...     \n keyword will try to find image on the screen from expected image first 
                    ...     \n then will try to click it
                    ...     \n default threshold to compare is 0.8 = 80%
                    ...     \n ``abs_expected_image_path`` is the absolute path of expected image to be clicked
    [Arguments]     ${abs_expected_image_path}      ${threshold}=0.8
    ${is_found_image}   ${xy}=  RainyAppCommon.Image should be visible on screen   ${expected_image}   ${threshold}=0.8
    
    IF      ${is_found_image}
        AppiumLibrary.Click element at coordinates     ${xy[0]}     ${xy[1]}
    ELSE
        Should be true  ${is_found_image}   msg="Image was not found on the screen"
    END

Press keycode numbers
    [Arguments]   ${numbers}
    ${conver_to_string}=   Convert to string   ${numbers}
    ${get_length}=    Get length   ${conver_to_string}
    FOR    ${i}    IN RANGE    0   ${get_length}
        ${num}=         Convert to integer   ${conver_to_string[${i}]}
        ${keycode}=     Evaluate    ${num}+7
        Press keycode   ${keycode}
    END

Enable appium ime keyboard using adb 
    AdbUtils.Enable ime keyboard using adb

Disable appium ime keyboard using adb 
    AdbUtils.Disable ime keyboard using adb

Press search button using adb
    AdbUtils.Press search button on appium ime using adb

Load android emulator snapshot using adb 
    [Arguments]     ${snapshot_name}
    AdbUtils.Load android emulator snapshot using adb    ${snapshot_name}

List android emulator snapshot using adb 
    AdbUtils.List android emulator snapshot using adb


Save android emulator snapshot using adb
    [Arguments]     ${snapshot_name} 
    AdbUtils.Save android emulator snapshot using adb        ${snapshot_name}

Push image file to emulator 
    [Arguments]     ${emulator_destination_path}    ${to_push_image_path}
    AppiumUtils.Push image file to emulator     ${emulator_destination_path}    ${to_push_image_path}

Image should be visible on screen   
    [Documentation]     Find image on current screen by comparing screenshot of current screen and expected image 
    ...     \n default threshold is 0.8 meaning 80% of 2 images should match 
    ...     \n Return true/false and xy of the expected image on screen if any
    ...     \n ``abs_expected_image_path`` is the absolute path of expected image 
    [Arguments]     ${abs_expected_image_path}   ${threshold}=0.8
    ${current_time}=            BuiltIn.Get time    epoch
    ${screen_screenshot}=       AppiumLibrary.Capture Page Screenshot     ${OUTPUT_DIR}${/}screen_screenshot_${current_time}.png
    ${is_found_image}   ${xy}=  ImageUtils.Image should be visible on screen
                                ...     ${abs_expected_image_path}
                                ...     ${screen_screenshot}
                                ...     ${threshold}
    [Return]    ${is_found_image}   ${xy}

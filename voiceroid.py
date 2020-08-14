# -*- coding: utf-8 -*-
import pywinauto
import os
import time

def search_child_byclassname(class_name, uiaElementInfo, target_all = False):
    target = []
    # 全ての子要素検索
    for childElement in uiaElementInfo.children():
        # ClassNameの一致確認
        if childElement.class_name == class_name:
            if target_all == False:
                return childElement
            else:
                target.append(childElement)
    if target_all == False:
        # 無かったらFalse
        return False
    else:
        return target


def search_child_byname(name, uiaElementInfo):
    # 全ての子要素検索
    print("search_child_byname: " + name)
    print(uiaElementInfo.children())
    for childElement in uiaElementInfo.children():
        # Nameの一致確認
        print(childElement.name)
        if childElement.name == name:
            return childElement
    # 無かったらFalse
    return False

def talkVOICEROID2(speakPhrase, filename):

    app = pywinauto.Application().start("C:\Program Files (x86)\AHS\VOICEROID2\VoiceroidEditor.exe")

    # デスクトップのエレメント
    parentUIAElement = pywinauto.uia_element_info.UIAElementInfo()
    # voiceroidを捜索する
    voiceroid2 = False
    while(voiceroid2 == False):
        voiceroid2 = search_child_byname("VOICEROID2",parentUIAElement)
        # *がついている場合
        if voiceroid2 == False:
            voiceroid2 = search_child_byname("VOICEROID2*",parentUIAElement)

    # テキスト要素のElementInfoを取得
    TextEditViewEle = search_child_byclassname("TextEditView",voiceroid2)
    textBoxEle      = search_child_byclassname("TextBox",TextEditViewEle)

    # コントロール取得
    textBoxEditControl = pywinauto.controls.uia_controls.EditWrapper(textBoxEle)

    # テキスト登録
    textBoxEditControl.set_edit_text(speakPhrase)


    # ボタン取得
    buttonsEle = search_child_byclassname("Button",TextEditViewEle,target_all = True)
    # 音声保存ボタンを探す
    playButtonEle = ""
    saveButtonEle = ""
    print("buttons")
    print(buttonsEle)

    for buttonEle in buttonsEle:
        # テキストブロックを捜索
        textBlockEle = search_child_byclassname("TextBlock", buttonEle)
        print("text")
        print(textBlockEle )

        if textBlockEle.name == "再生":
            playButtonEle = buttonEle

        if textBlockEle.name == "音声保存":
            saveButtonEle = buttonEle


    # ボタンコントロール取得
    #playButtonControl = pywinauto.controls.uia_controls.ButtonWrapper(playButtonEle)
    saveButtonControl = pywinauto.controls.uia_controls.ButtonWrapper(saveButtonEle)

    # 再生ボタン押下
    #playButtonControl.click()
    # 音声保存ボタン押下
    saveButtonControl.click()

    voice_save_window = search_child_byname("音声保存",voiceroid2)
    if (voice_save_window):
        print(voice_save_window)
        print(voice_save_window.children())
        buttonsEle = search_child_byclassname("Button",voice_save_window,target_all = True)
        print("text")
        for buttonEle in buttonsEle:
            # テキストブロックを捜索

            if buttonEle.name == "OK":
                okButtonEle = buttonEle
                break
        # ボタンコントロール取得
        okButtonControl = pywinauto.controls.uia_controls.ButtonWrapper(okButtonEle)

        # OKボタン押下
        okButtonControl.click()
    else:
        voice_save_window = voiceroid2
    save_as_window = search_child_byname("名前を付けて保存", voice_save_window)
    print(save_as_window)
    print(save_as_window.children())



    Eles = search_child_byclassname("DUIViewWndClassName", save_as_window, target_all=True)
    print(Eles)
    for Ele in Eles:
        AppEles = search_child_byclassname("AppControlHost", Ele, target_all=True)
        for AppEle in AppEles:
            if AppEle.name == "ファイル名:":
                EditEles = search_child_byclassname("Edit", AppEle)

    print(EditEles)
    EditControl = pywinauto.controls.uia_controls.EditWrapper(EditEles)

    # ファイルの絶対パスを「ファイル名：」に書き出し
    voice_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), filename)
    EditControl.set_edit_text(voice_path)

    buttonsEle = search_child_byclassname("Button",save_as_window,target_all = True)
    print(buttonsEle)
    for buttonEle in buttonsEle:
        # テキストブロックを捜索
        if buttonEle.name == "保存(S)":
            saveButtonEle = buttonEle

    # ボタンコントロール取得
    saveButtonControl = pywinauto.controls.uia_controls.ButtonWrapper(saveButtonEle)

    # 保存ボタン押下
    saveButtonControl.click()

    print (save_as_window.children())

    # 上書き確認ダイアログ
    over_write_window = search_child_byname("名前を付けて保存", save_as_window)
    if (over_write_window):
        print(over_write_window.children())

        buttonsEle = search_child_byclassname("Button",over_write_window,target_all = True)
        print(buttonsEle)
        yesButtonEle = False
        for buttonEle in buttonsEle:
            # テキストブロックを捜索
            if buttonEle.name == "はい(Y)":
                yesButtonEle = buttonEle
        if (yesButtonEle):
            # ボタンコントロール取得
            yesButtonControl = pywinauto.controls.uia_controls.ButtonWrapper(yesButtonEle)

            # Yesボタン押下
            yesButtonControl.click()


    info_window = False
    voice_save_window = search_child_byname("音声保存",voiceroid2)
    while(info_window == False):
        info_window = search_child_byname("情報", voice_save_window)
    print(voice_save_window.children())
    print(info_window.children())

    buttonsEle = search_child_byclassname("Button",info_window)
    yesButtonControl = pywinauto.controls.uia_controls.ButtonWrapper(buttonsEle)

    # Yesボタン押下
    yesButtonControl.click()
if __name__ == "__main__":
    talkVOICEROID2("test", os.path.join("tmpdata", "voice.wav"))
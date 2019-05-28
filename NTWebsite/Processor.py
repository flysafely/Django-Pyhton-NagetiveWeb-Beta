from NTWebsite.improtFiles.processor_import_head import *
from NTWebsite.improtFiles.models_import_head import *
from NTWebsite.Config import AppConfig as AC
from NTWebsite.Config import DBConfig as DC


def indexView(request):
    APPConf = AC()
    return HttpResponseRedirect(APPConf.IndexURL)


def PaginatorInfoGet(objects, number, URLParams):
    if objects:
        ObjectsPaginator = Paginator(list(objects), number)
        ObjectList = Paginator(list(objects), number).page(
            int(URLParams['PageNumber']))
        Paginator_num_pages = ObjectsPaginator.num_pages
        Paginator_href = "/%s/%s/%s/%s/" % (
            URLParams['Region'], URLParams['Part'], URLParams['FilterValue'], URLParams['Order'])
        return {'ObjectList': ObjectList, 'ObjectsPaginator': ObjectsPaginator, 'Paginator_num_pages': Paginator_num_pages, 'Paginator_Href': Paginator_href}
    else:
        return {'ObjectList': [], 'ObjectsPaginator': '', 'Paginator_num_pages': 0, 'Paginator_Href': ''}


def NoticeCount(request):
    return str(QRC('Notice.objects.filter(TargetUser=%s).count()', None, request.user)) if request.user.is_authenticated else '0'


def FetchTopic(request):
    if request.method == 'POST':
        if request.user.is_authenticated:
            TopicObject = QRC('TopicInfo.objects.get(ObjectID=%s)',
                              0, request.POST.get('TopicID'))
            TopicID = str(TopicObject.ObjectID)
            Title = TopicObject.Title
            Content = TopicObject.Content
            Category = TopicObject.Category.Name
            themes = []
            for theme in TopicObject.Theme.all():
                themes.append(theme.Name)
            Themes = '&'.join(themes)
            jsondata = json.dumps({'TopicID': TopicID, 'Title': Title, 'Content': Content,
                                   'Category': Category, 'Themes': Themes}, ensure_ascii=False)
            return HttpResponse(jsondata)


def PublishTopic(request):
    if request.method == 'POST':
        if request.user.is_authenticated:
            InsertDataDict = {'Title': request.POST.get('Title'),
                              'Category': request.POST.get('Category'),
                              'Content': request.POST.get('Content'),
                              'Description': request.POST.get('Description'), }
            TopicID = request.POST.get('TopicID')
            Themes = request.POST.get('Themes')
            InsertDataDict['Category'] = QRC(
                'TopicCategoryInfo.objects.get(Name=%s)', None, InsertDataDict['Category'])
            # 将主题按&分割后使用get_or_create有就返回，没有就创建了返回
            ThemeObjects = []
            for Theme in Themes.split('&'):
                ThemeObjects.append(
                    QRC('TopicThemeInfo.objects.get_or_create(Name=%s)', None, Theme)[0])
            try:
                # 放在try里面执行，避免图片被移动后，检查出标题重复的问题
                InsertDataDict['Content'] = mMs.MovePicToSavePath(
                    InsertDataDict['Content'])
                # 如果Topic有值则为编辑文章
                if TopicID:
                    mMs.RemovePicFromSavePath(
                        TopicID, InsertDataDict['Content'])
                    Topic = TopicInfo.objects.filter(
                        ObjectID=TopicID).update(**InsertDataDict)
                    Topic = TopicInfo.objects.get(ObjectID=TopicID)
                else:
                    # 不用QRC的原因是ContentText文章中的引号容易出现问题!
                    Topic = TopicInfo.objects.create(ObjectID=mMs.CreateUUIDstr(),
                                                     Title=InsertDataDict[
                                                         'Title'],
                                                     Content=InsertDataDict[
                                                         'Content'],
                                                     Description=InsertDataDict[
                                                         'Description'],
                                                     Category=InsertDataDict[
                                                         'Category'],
                                                     Publisher=request.user,)
                Topic.Theme.clear()
                Topic.Theme.add(*ThemeObjects)
                Topic.save()
                return HttpResponse('ok')
            except Exception as e:
                return HttpResponse(str(e) + "验证！")
        else:
            return HttpResponse('login')


def PublishRollCall(request):
    if request.user.is_authenticated:
        RollCallTitle = request.POST.get('RollCallTitle')
        TargetUserNick = request.POST.get('TargetUserNick')
        RollCallContent = request.POST.get('RollCallContent')
        TargetUser = QRC('User.objects.get(Nick=%s)', None, TargetUserNick)
        BlackListRecord = QRC(
            'BlackList.objects.filter(Enforceder=%s,Handler=%s)', None, request.user, TargetUser)
        if TargetUser:
            if BlackListRecord:
                return HttpResponse("用户:'" + TargetUserNick + "'" + '已经屏蔽您!')
            else:
                try:
                    NewRollCall = QRC('RollCallInfo.objects.create(Title=%s,Publisher=%s,Target=%s,ObjectID=%s)', 0,
                                      RollCallTitle, request.user, QRC('User.objects.get(Nick=%s)', None, TargetUserNick), mMs.CreateUUIDstr())
                    NewDialogue = QRC(
                        'RollCallDialogue.objects.create(RollCallID=%s,Publisher=%s,Content=%s,ObjectID=%s)', 0, NewRollCall, request.user, RollCallContent, mMs.CreateUUIDstr())
                    return HttpResponse('publishok')
                except Exception as e:
                    if 'UNIQUE' in str(e):
                        return HttpResponse('titleisexisted')
                    else:
                        raise e
        else:
            return HttpResponse("用户:'" + TargetUserNick + "'" + '不存在!')
    else:
        return HttpResponse('login')


def ContextConfirm(request, **Params):
    NotificationCount = NoticeCount(request)
    # 文章分类信息获取
    CategoryList = QRC('TopicCategoryInfo.objects.all()', None)
    # 推荐发布者信息获取
    PublisherList = QRC("PublisherList.objects.all()", None)
    # 生成上下文字典
    ContextDict = {"Layout_Sizer": Params['URLParams'],
                   "Main_URL_Sizer": {'Topic': ('is-active', '', ''), 'RollCall': ('', 'is-active', ''), 'SpecialTopic': ('', '', 'is-active'), 'UserProfile': ('', '', ''), 'Search': ('', '', '')}[Params['URLParams']['Region']],
                   "ExportItem_UserInfo": Params['User'] if 'User' in Params else '',
                   "Export_Object": Params['MainObject'] if 'MainObject' in Params else '',
                   "ExportList_Topic": Params['Object'] if 'Object' in Params else '',
                   "ExportList_Cards": Params['PaginatorDict']['ObjectList'] if 'PaginatorDict' in Params else '',
                   "ExportList_Categorys": CategoryList,
                   "ExportList_Publishers": PublisherList,
                   "Paginator_num_pages": Params['PaginatorDict']['Paginator_num_pages'] if 'PaginatorDict' in Params else '',
                   "Current_Pagenumber": Params['URLParams']['PageNumber'] if 'URLParams' in Params else '',
                   "Paginator_Href": Params['PaginatorDict']['Paginator_Href'] if 'PaginatorDict' in Params else '',
                   "Search_Placeholder": Params['APPConf'].TopicHotKeyWord if 'APPConf' in Params else '',
                   "NotificationCount": NotificationCount}
    return ContextDict


def CommentPackage(CommentObjects):
    if CommentObjects:
        CommentCards = []
        for CommentObject in CommentObjects:
            if CommentObject[0].Parent:
                CommentCards.append(
                    ('1', CommentObject[0].Parent, CommentObject))
            else:
                CommentCards.append(('0', '', CommentObject))
        return CommentCards
    else:
        return 0


def ReadIPRecord(IP, ID, type):
    ReadsIP.objects.get_or_create(IP=IP, ObjectID=ID, Type=type)


def AttitudeOperate(request):
    Type = 'Topic' if request.POST.get(
        'Type') in 'SpecialTopic' else request.POST.get('Type')
    Object = QRC(Type + 'Info.objects.get(ObjectID=%s)',
                 None, request.POST.get('ObjectID'))
    Point = request.POST.get('Point')

    if request.user.is_authenticated:
        record = QRC(('Topic' if Type in 'SpecialTopic' else 'Comment') +
                     'Attitude.objects.filter(ObjectID=%s,Type=%s,Publisher=%s)', 0, Object, Type, request.user)
        if record and len(record) < 2:
            if record[0].Point == int(Point):
                record[0].delete()
                return HttpResponse('Cancel')
            else:
                record[0].Point = int(Point)
                record[0].save()
                return HttpResponse('Become')
        elif record and len(record) > 2:
            for item in record:
                item.delete()
        else:
            QRC(('Topic' if Type in 'SpecialTopic' else 'Comment') +
                'Attitude.objects.create(ObjectID=%s,Type=%s,Publisher=%s,Point=%s)', 0, Object, Type, request.user, int(Point))
            return HttpResponse('Confirm')
    else:
        return HttpResponse('login')


@csrf_exempt
def UploadImg(request):
    if request.method == 'POST':
        return HttpResponse(mMs.PicUploadOperate(request.FILES['upload']))


def TipOff(request):
    if request.method == 'POST':
        Type = request.POST.get('Type')
        TopicID = request.POST.get('TopicID')
        Content = request.POST.get('Content')
        if request.user.is_authenticated:
            userObject = QRC('User.objects.get(id=%s)', None, request.user.id)
            TipOffObject = QRC(
                'TipOffBox.objects.filter(ObjectID=%s,Publisher=%s)', 0, TopicID, userObject)
            if TipOffObject:
                return HttpResponse('cancel')
            else:
                QRC('TipOffBox.objects.create(ObjectID=%s, Publisher=%s, Type=%s, Content=%s)',
                    0, TopicID, userObject, Type, Content)
                return HttpResponse('success')
        else:
            return HttpResponse('login')


def Replay(request):
    if request.method == 'POST':
        temp_Map = {'Topic': 'TRCount',
                    'SpecialTopic': 'SRCount', 'RollCall': 'RCount'}
        Type = request.POST.get('Type')
        ObjectID = request.POST.get('ObjectID')
        TopicObject = QRC('TopicInfo.objects.get(ObjectID=%s)',
                          None, request.POST.get('ObjectID'))
        Content = request.POST.get('Content')
        ParentID = request.POST.get('ParentID')
        if request.user.is_authenticated:
            if Type in 'SpecialTopic':
                ReplayObject = QRC('CommentInfo.objects.create(ObjectID=%s, TopicID=%s,Content=%s,Parent=%s,Type=%s,Publisher=%s)',
                                   0, mMs.CreateUUIDstr(), TopicObject, Content, QRC('CommentInfo.objects.get(ObjectID=%s)', None, ParentID), Type, request.user)
            else:
                RollCall = QRC(
                    'RollCallInfo.objects.get(ObjectID=%s)', None, ObjectID)
                ReplayObject = QRC('RollCallDialogue.objects.create(ObjectID=%s,RollCallID=%s,Content=%s,Display=%s,Publisher=%s)',
                                   0, mMs.CreateUUIDstr(), RollCall, Content, '' if RollCall.Publisher == request.user else 'right', request.user)
                if not RollCall.Publisher == request.user:
                    pass
            return HttpResponse('replayok')
        else:
            return HttpResponse('login')


def Collect(request):
    if request.user.is_authenticated:
        Type = request.POST.get('Type')
        Object = QRC(('Topic' if Type in 'CollectConcern' else 'RollCall') +
                     'Info.objects.get(ObjectID=%s)', 0, request.POST.get('ObjectID'))

        result = QRC(
            Type + '.objects.filter(Publisher=%s,ObjectID=%s)', 0, request.user, Object)
        if not result:
            QRC(Type + '.objects.create(Publisher=%s,ObjectID=%s)',
                0, request.user, Object)
            return HttpResponse(Type)
        else:
            result[0].delete()
            return HttpResponse(Type + 'Cancel')
    else:
        return HttpResponse('login')


def StatisticalDataUpdata(objectStr, methodDsc):
    exec(objectStr + methodDsc)
    exec(objectStr + '.save()')


def Param(request):
    if request.method == "GET":
        KeyWord = request.GET.get('KeyWord')
        if KeyWord == 'SecretKey':
            APPConf = AC()
            jsondata = json.dumps(
                [APPConf.SecretKey, APPConf.SecretVI], ensure_ascii=False)
            return HttpResponse(jsondata)
        else:
            pass

# 新用户激活


def UserActive(userid, key):
    APPConf = AC()
    print('userid:',userid)
    print(mMs.RedisCacheOperation('get',TimeOut=0,key=key))
    if userid == mMs.RedisCacheOperation('get',TimeOut=0,key=key):
        UserObject=User.objects.get(id=int(userid))
        UserObject.is_active=True
        UserObject.save()
        mMs.RedisCacheOperation('delete',TimeOut=0, key=key)
        return HttpResponseRedirect(APPConf.IndexURL)
    else:
        return HttpResponse('未匹配')
    # 用户登录


def Login(request):
    if request.method == 'POST':
        # 注册信息获取
        username = mMs.Decrypt(mMs.DecodeWithBase64(
            request.POST.get('username')))
        userpassword = mMs.Decrypt(
            mMs.DecodeWithBase64(request.POST.get('password')))
        user = auth.authenticate(username=username, password=userpassword)

        if user:
            login(request, user)
            return HttpResponse(True)
        else:
            return HttpResponse("")

# 忘记密码


def ChangePassWord(request):
    if request.method == 'POST':
        username = mMs.Decrypt(mMs.DecodeWithBase64(
            request.POST.get('username')))
        email = mMs.Decrypt(mMs.DecodeWithBase64(request.POST.get('email')))

# 注册界面


def Regist(request):
    APPConf = AC()
    if request.method == 'POST':
        username = mMs.Decrypt(mMs.DecodeWithBase64(
            request.POST.get('username')))
        usernickname = mMs.Decrypt(mMs.DecodeWithBase64(
            request.POST.get('usernickname')))
        password = mMs.Decrypt(mMs.DecodeWithBase64(
            request.POST.get('password')))
        email = mMs.Decrypt(mMs.DecodeWithBase64(request.POST.get('email')))
        try:
                # 这里通过前端注册账号一定要是要create_user 不然后期登录的时候
                # auth.authenticate无法验证用户名和密码
            newUser = User.objects.create_user(
                username, Nick=usernickname, password=password, email=email, is_active=False)
            mMs.SendMail('regist', newUser)
            newUser.Avatar = mMs.UserAvatarOperation(request.POST.get(
                'userimagedata'), request.POST.get('userimageformat'), APPConf.DefaultAvatar.url.replace(settings.MEDIA_URL, ''))['Path']
            newUser.save()
            return HttpResponse('ok')

        except Exception as e:
            return HttpResponse(str(e))


def Logout(request):
    if request.method == 'GET':
        if request.user.is_authenticated:
            auth.logout(request)
            return HttpResponse('Logout')
        else:
            return HttpResponse('logouted')
    else:
        return HttpResponse('not get')


def AddNotification(Region, ObjectID, AnchorID, TargetUser, SourceUser):
    try:
        QRC('Notification.objects.create(ID=%s, Region=%s, ObjectID=%s, AnchorID=%s, TargetUser=%s, SourceUser=%s)',
            0, mMs.CreateUUIDstr(), Region, ObjectID, AnchorID, TargetUser, SourceUser)
    except Exception as e:
        raise e


@csrf_exempt
def NoticeOpreate(request):
    if request.method == 'GET':
        return NoticeGet(request)
    elif request.method == 'DELETE':
        return NoticeDelete(request)


def BlackListOperation(request):
    if request.method == 'POST':
        UserID = request.POST.get('UserID')
        Operation = request.POST.get('Operation')
        UserObject = QRC('User.objects.get(id=%s)', None, UserID)
        if request.user.is_authenticated and Operation == 'add':
            try:
                if not QRC('BlackList.objects.filter(Enforceder=%s, Handler=%s)', 0, UserObject, request.user):
                    BlackList.objects.create(ID=mMs.CreateUUIDstr(
                    ), Enforceder=UserObject, Handler=request.user)
                return HttpResponse('add')
            except Exception as e:
                return HttpResponse(e)

        elif request.user.is_authenticated and Operation == 'delete':
            try:
                QRC('BlackList.objects.get(Enforceder=%s,Handler=%s)',
                    0, UserObject, request.user).delete()
                return HttpResponse('delete')
            except Exception as e:
                return HttpResponse(e)
        else:
            return HttpResponse('login')


def UserLink(request):
    Operation = request.POST.get('Operation')
    if request.method == 'POST':
        if request.user.is_authenticated:
            UserID = request.POST.get('UserID')
            UserObject = QRC('User.objects.get(id=%s)', None, UserID)
            try:
                if Operation == 'add':
                    QRC('UserLink.objects.get_or_create(UserBeLinked=%s,UserLinking=%s)',
                        0, UserObject, request.user)
                    #UserLink.objects.get_or_create(UserBeLinked=UserObject, UserLinking=request.user)
                    return HttpResponse('add')
                elif Operation == 'delete':
                    QRC('UserLink.objects.get(UserBeLinked=%s,UserLinking=%s)',
                        0, UserObject, request.user).delete()
                    return HttpResponse('delete')
            except Exception as e:
                return HttpResponse(e)
        else:
            return HttpResponse('login')


def UserProfileUpdate(request):
    APPConf = AC()
    if request.method == 'POST':
        UserImageData = request.POST.get('UserImageData')
        UserImageFormat = request.POST.get('UserImageFormat')
        UserNickName = request.POST.get('UserNickName')
        UserDescription = request.POST.get('UserDescription')
        UserSex = request.POST.get('UserSex')
        UserConstellation = request.POST.get('UserConstellation')
        UserEmail = request.POST.get('UserEmail')
        UserRegion = request.POST.get('UserRegion')
        userObject = QRC('User.objects.get(Nick=%s)', 0, request.user.Nick)
        if QRC('User.objects.get(Nick=%s)', 0, UserNickName) and QRC('User.objects.get(Nick=%s)', 0, UserNickName) != request.user:
            return HttpResponse('Nick')
        else:
            UploadImage_Operated = ''
            UploadImage_Operated = mMs.UserAvatarOperation(
                UserImageData, UserImageFormat, userObject.Avatar)
            userObject.Avatar = UploadImage_Operated['Path']
            userObject.Nick = UserNickName
            userObject.Sex = UserSex
            userObject.Region = UserRegion
            userObject.email = UserEmail
            userObject.Description = UserDescription
            userObject.Constellation = UserConstellation
            userObject.save()
            return HttpResponse(UploadImage_Operated['Status'])


if __name__ == "__main__":
    print('%s' % 'abc')

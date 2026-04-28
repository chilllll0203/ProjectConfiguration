from datetime import datetime
from fastapi import APIRouter, Request, Form, Depends, HTTPException
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse, RedirectResponse
from deps import get_session
from models import AchievementModel, EventModel
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

router = APIRouter()
templates = Jinja2Templates(directory="templates")


@router.get("/profile")
def profile(request: Request):
    role = request.session["role"]
    if (role == "student"):
        return templates.TemplateResponse(request,"personal_account_student.html")
    elif (role == "teacher"):
        return templates.TemplateResponse(request,"personal_account_teacher.html")
    elif (role == "administrator"):
        return templates.TemplateResponse(request,"personal_account_administrator.html")
    else:
        return "Произошла ошибка попробуйте снова!"

@router.get("/settings")
def settings(request: Request):
    role = request.session["role"]
    if (role == "student"):
        return templates.TemplateResponse(request, "settingsstudent.html")
    elif (role == "teacher"):
        return templates.TemplateResponse(request, "settingsteacher.html")
    elif (role == "administrator"):
        return templates.TemplateResponse(request, "settingsadmin.html", {"username":request.session["username"],"email":request.session["email"]})
    else:
        return "Произошла ошибка попробуйте снова!"

@router.get("/achievements")
def achievements(request: Request):
    role = request.session["role"]
    if (role != "student"):
        raise  HTTPException(status_code=403,detail="Access forbidden")
    return templates.TemplateResponse(request, "achievements.html")

# @router.post("/tg_auth")
# def tg_auth(request: Request):

# @router.get("/person_account_student")
# def person_account_student(request: Request):
#     return templates.TemplateResponse(request, "personal_account_student.html")
# @router.post("/person_account_student")
# def person_account_student_post(request: Request, option: str = Form(...)):
#     username = request.session["username"]
#     email = request.session["email"]
#     if option == "home":
#         return templates.TemplateResponse(request, "personal_account_student.html", {"username": username, "email": email})
#     elif option == "view_your_achievements":
#         return RedirectResponse("/view_your_achievements", status_code=303)
#     elif option == "add_achievements":
#         return templates.TemplateResponse(request, "add_achievements.html")
#     elif option == "settings":
#         return templates.TemplateResponse(request, "settingsstudent.html", {"username": username, "email": email})
#
#
# @router.get("/person_account_teacher")
# def person_account_teacher(request: Request):
#     return templates.TemplateResponse(request, "personal_account_teacher.html")
# @router.post("/person_account_teacher")
# def person_account_teacher_post(request: Request, option: str = Form(...)):
#     username = request.session["username"]
#     email = request.session["email"]
#     if option == "home":
#         return templates.TemplateResponse(request, "personal_account_teacher.html", {"username": username, "email": email})
#     elif option == "view_all_events":
#         return RedirectResponse("/events", status_code=303)
#     elif option == "add_event":
#         return templates.TemplateResponse(request, "add_event.html")
#     elif option == "settings":
#         return templates.TemplateResponse(request, "settingsteacher.html", {"username": username, "email": email})
#
#
# @router.get("/person_account_administrator")
# def person_account_administrator(request: Request):
#     return templates.TemplateResponse(request, "personal_account_administrator.html")
# @router.post("/person_account_administrator")
# def person_account_administrator_post(request: Request, option: str = Form(...)):
#     username = request.session["username"]
#     email = request.session["email"]
#     if option == "home":
#         return templates.TemplateResponse(request, "personal_account_administrator.html",{"username": username, "email": email})
#     elif option == "table_users":
#         return RedirectResponse("/users", status_code=303)
#     elif option == "table_events":
#         return RedirectResponse("/events", status_code=303)
#     elif option == "table_achievements":
#         return RedirectResponse("/achievements", status_code=303)
#     elif option == "settings":
#         return templates.TemplateResponse(request, "settingsadmin.html", {"username": username, "email": email})
#
#
# @router.get("/settingsadmin")
# def settings_admin(request: Request):
#     username = request.session["username"]
#     email = request.session["email"]
#     return templates.TemplateResponse(request, "settingsadmin.html", {"username": username, "email": email})
# @router.post("/settingsadmin")
# def settings_admin_post(request: Request, option: str = Form(None), changepassword: str = Form(None), exitaccount: str = Form(None)):
#     username = request.session["username"]
#     email = request.session["email"]
#     if option == "home":
#         return templates.TemplateResponse(request, "personal_account_administrator.html",{"username": username, "email": email})
#     elif option == "table_users":
#         return RedirectResponse("/users", status_code=303)
#     elif option == "table_events":
#         return RedirectResponse("/events", status_code=303)
#     elif option == "table_achievements":
#         return RedirectResponse("/achievements", status_code=303)
#     elif option == "settings":
#         return templates.TemplateResponse(request, "settingsadmin.html", {"username": username, "email": email})
#     if changepassword:
#         return {"message": "Пока эта функция не реализована!"}
#     if exitaccount:
#         request.session.clear()
#         return templates.TemplateResponse(request, "extrance.html")
#
#
#
# @router.get("/add_achievements")
# def add_achievements_get(request: Request):
#     return templates.TemplateResponse(request, "add_achievements.html")
# @router.post("/add_achievements")
# async def add_achievements_post(
#         request: Request,
#         option: str = Form(None),
#         nameEvent: str = Form(None),
#         category: str = Form(None),
#         result_achievement: str = Form(None),
#         document_url: str = Form(None),
#         addachievement: str = Form(None),
#         session: AsyncSession = Depends(get_session)
# ):
#     username = request.session["username"]
#     email = request.session["email"]
#     if option == "home":
#         return templates.TemplateResponse(request, "personal_account_student.html",{"username": username, "email": email})
#     elif option == "view_your_achievements":
#         return RedirectResponse("/view_your_achievements", status_code=303)
#     elif option == "add_achievements":
#         return templates.TemplateResponse(request, "add_achievements.html")
#     elif option == "settings":
#         return templates.TemplateResponse(request, "settingsstudent.html", {"username": username, "email": email})
#     if addachievement == "addachievement":
#         result = await session.execute(select(EventModel).where(EventModel.title == nameEvent))
#         event = result.scalars().first()
#         if event:
#             achievement = AchievementModel(
#                 student_id=request.session["user_id"],
#                 event_id=event.id,
#                 category=category,
#                 result=result_achievement,
#                 document_url=document_url,
#                 created_at=datetime.now()
#             )
#             session.add(achievement)
#             await session.commit()
#         return RedirectResponse("/view_your_achievements", status_code=303)
#
#
#
# @router.get("/add_event")
# def add_event_get(request: Request):
#     return templates.TemplateResponse(request, "add_event.html")
# @router.post("/add_event")
# async def add_event_post(
#         request: Request,
#         option: str = Form(None),
#         title: str = Form(...),
#         description: str = Form(...),
#         event_date: str = Form(...),
#         type: str = Form(...),
#         addevent: str = Form(None),
#         session: AsyncSession = Depends(get_session)
# ):
#     username = request.session["username"]
#     email = request.session["email"]
#     if option == "home":
#         return templates.TemplateResponse(request, "personal_account_teacher.html",
#                                           {"username": username, "email": email})
#     elif option == "view_all_events":
#         return RedirectResponse("/events", status_code=303)
#     elif option == "add_event":
#         return templates.TemplateResponse(request, "add_event.html")
#     elif option == "settings":
#         return templates.TemplateResponse(request, "settingsteacher.html", {"username": username, "email": email})
#     if addevent == "addevent":
#         event = EventModel(
#             title=title,
#             description=description,
#             event_date=datetime.strptime(event_date, '%Y-%m-%d').date(),
#             type=type,
#             created_by=request.session["user_id"],
#             created_at=datetime.now()
#         )
#         session.add(event)
#         await session.commit()
#         return RedirectResponse("/events", status_code=303)
#
#
#
# @router.get("/settingsstudent")
# def settings_student_get(request: Request):
#     username = request.session["username"]
#     email = request.session["email"]
#     return templates.TemplateResponse(request, "settingsstudent.html", {"username": username, "email": email})
# @router.post("/settingsstudent")
# def settings_student_post(request: Request, option: str = Form(None), changepassword: str = Form(None),exitaccount: str = Form(None)):
#     username = request.session["username"]
#     email = request.session["email"]
#     if option == "home":
#         return templates.TemplateResponse(request, "personal_account_student.html",{"username": username, "email": email})
#     elif option == "view_your_achievements":
#         return RedirectResponse("/view_your_achievements", status_code=303)
#     elif option == "add_achievements":
#         return templates.TemplateResponse(request, "add_achievements.html")
#     elif option == "settings":
#         return templates.TemplateResponse(request, "settingsstudent.html", {"username": username, "email": email})
#     if changepassword:
#         return {"message": "Пока эта функция не реализована!"}
#     if exitaccount:
#         request.session.clear()
#         return templates.TemplateResponse(request, "extrance.html")
#
#
#
# @router.get("/settingsteacher")
# def settings_teacher_get(request: Request):
#     username = request.session["username"]
#     email = request.session["email"]
#     return templates.TemplateResponse(request, "settingsteacher.html", {"username": username, "email": email})
# @router.post("/settingsteacher")
# def settings_teacher_post(request: Request, option: str = Form(None), changepassword: str = Form(None),exitaccount: str = Form(None)):
#     username = request.session["username"]
#     email = request.session["email"]
#     if option == "home":
#         return templates.TemplateResponse(request, "personal_account_teacher.html",{"username": username, "email": email})
#     elif option == "view_all_events":
#         return RedirectResponse("/events", status_code=303)
#     elif option == "add_event":
#         return templates.TemplateResponse(request, "add_event.html")
#     elif option == "settings":
#         return templates.TemplateResponse(request, "settingsteacher.html", {"username": username, "email": email})
#     if changepassword:
#         return {"message": "Пока эта функция не реализована!"}
#     if exitaccount:
#         request.session.clear()
#         return templates.TemplateResponse(request, "extrance.html")

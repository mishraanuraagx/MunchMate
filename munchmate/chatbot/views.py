import random
import openai
from django.http import JsonResponse
from recipes.models import Recipe
from .models import Conversation
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render
import json

from django.http import HttpRequest
from django.test import RequestFactory
from django.urls import reverse

import re
from django.utils.safestring import mark_safe

api_key = ""
client = openai.OpenAI(api_key=api_key)


# APIs
def chatbot_home(request):
    return JsonResponse({"message": "Welcome to MunchMate! Your partner for popular recipe search."})


# API: Handle User Chat & Save to DB
@csrf_exempt
def chatbot_view(request):
    if request.method == "POST":
        data = json.loads(request.body)
        user_message = data.get("message", "").lower()

        # todo: use encoder model to learn more about the recipe requirement, user may enter ambiguous requirements
        # by default keeping recipe_type to vegetarian
        recipe_type = 2
        if "vegan" in user_message:
            recipe_type = 1
        elif "nonveg" in user_message or "non-veg" in user_message or "non veg" in user_message:
            recipe_type = 3

        # Get 3 random recipes of the specified type
        # Note for me: ? shuffles the entire list first, and then perform get call -> point for optimization
        recipes = list(Recipe.objects.filter(recipe_type=recipe_type).order_by("?")[:3])

        if not recipes:
            recipe_type_name = Recipe.RECIPE_TYPES[recipe_type]
            chatbot_response = f"Sorry, I couldn't find any {recipe_type_name[1]} recipe(s) in my database. I will let my creator know that someone is looking for this stuff. Check back later!"
        else:
            recipe_info = "\n\n".join(
                [f"Recipe Name- {recipe.name}, \nRecipe Details - {recipe.details}" for recipe in recipes])
            # depending on the use case, we can further add original user_query for more personalised reply. Maybe!
            prompt = "\nUser query : " + user_message + \
                     f"\n\nUser asked for {recipe_type} recipes. Here are three options:\n{recipe_info} \n\n" + \
                     "\n\n You are MunchMate! A friendly foodie who suggest recipes customized to user query." + \
                     "\nCan you provide a response in a friendly tone? Mention these are you favorite recipes." + \
                     "\n Add more info about the recipe if missing." + \
                     "\n For final response, try to involve original user query" + \
                     "only if query is relevant to food related conversation." + \
                     "\n In the end say, hope this helps, have a nice day."

            completion = client.beta.chat.completions.parse(
                model="gpt-4o",
                messages=[
                    {"role": "system", "content": "You are a helpful assistant."},
                    {"role": "user", "content": prompt},
                ],
                response_format={
                    "type": "text"
                },
                temperature=1,
                max_completion_tokens=2048,
                top_p=1,
                frequency_penalty=0,
                presence_penalty=0
            )

            chatbot_response = completion.choices[0].message.content
            if chatbot_response:
                formatted_res = format_response(chatbot_response)
                # todo: add the logged in user details
                Conversation.objects.create(sender="MunchMate_v0.1", recipient="User", message=user_message,
                                            response=formatted_res)

        chatbot_response = format_bolden(chatbot_response)
        return JsonResponse({"response": chatbot_response})

    elif request.method == "GET":
        # return JsonResponse({"content": "chat history"})
        return get_all_chats(request)

    return JsonResponse({"error": "Invalid request"}, status=400)

@csrf_exempt
def simulate_conversation(request):
    if request.method == "POST":
        data = json.loads(request.body)
        count = data.get("count", "")
        if type(count) is not int or (count > 10 or count < 1):
            return JsonResponse({"error": "Invalid request. Only integer values for allowed between 0 and 10"},
                                status=400)

        for counter in range(count):
            prompt = "\nImagine you are a user with a name, any name you can image. You wanna know about some favorite food or recipe from another user. Ask a one or two line question, on what is their favorite food, or ask them about some suggestion on vegetarian or vegan type foods. Make sure to keep the response within 2 sentences."

            completion = client.beta.chat.completions.parse(
                model="gpt-4o",
                messages=[
                    {"role": "system", "content": "You are a helpful assistant."},
                    {"role": "user", "content": prompt},
                ],
                response_format={
                    "type": "text"
                },
                temperature=1.5,
                max_completion_tokens=100,
                top_p=1,
                frequency_penalty=0,
                presence_penalty=0
            )
            chatbot_response = completion.choices[0].message.content
            if chatbot_response:
                # request = HttpRequest()
                # request.method = "POST"
                # request.POST = {"message": "chatbot_response"}
                # chatbot_view(request)
                # by default keeping recipe_type to vegetarian
                # todo: refactor this code
                user_message = chatbot_response
                recipe_type = 2
                if "vegan" in user_message:
                    recipe_type = 1
                elif "nonveg" in user_message or "non-veg" in user_message or "non veg" in user_message:
                    recipe_type = 3

                # Get 3 random recipes of the specified type
                # Note for me: ? shuffles the entire list first, and then perform get call -> point for optimization
                recipes = list(Recipe.objects.filter(recipe_type=recipe_type).order_by("?")[:3])

                if not recipes:
                    recipe_type_name = Recipe.RECIPE_TYPES[recipe_type]
                    chatbot_response = f"Sorry, I couldn't find any {recipe_type_name[1]} recipe(s) in my database. I will let my creator know that someone is looking for this stuff. Check back later!"
                else:
                    recipe_info = "\n\n".join(
                        [f"Recipe Name- {recipe.name}, \nRecipe Details - {recipe.details}" for recipe in recipes])
                    # depending on the use case, we can further add original user_query for more personalised reply. Maybe!
                    prompt = "\nUser query : " + user_message + \
                             f"\n\nUser asked for {recipe_type} recipes. Here are three options:\n{recipe_info} \n\n" + \
                             "\n\n You are MunchMate! A friendly foodie who suggest recipes customized to user query." + \
                             "\nCan you provide a response in a friendly tone? Mention these are you favorite recipes." + \
                             "\n Add more info about the recipe if missing." + \
                             "\n For final response, try to involve original user query" + \
                             "only if query is relevant to food related conversation." + \
                             "\n In the end say, hope this helps, have a nice day."

                    completion = client.beta.chat.completions.parse(
                        model="gpt-4o",
                        messages=[
                            {"role": "system", "content": "You are a helpful assistant."},
                            {"role": "user", "content": prompt},
                        ],
                        response_format={
                            "type": "text"
                        },
                        temperature=1.2,
                        max_completion_tokens=2048,
                        top_p=1,
                        frequency_penalty=0,
                        presence_penalty=0
                    )

                    chatbot_response = completion.choices[0].message.content
                    if chatbot_response:
                        formatted_res = format_response(chatbot_response)
                        # todo: add the logged in user details
                        Conversation.objects.create(sender="MunchMate_v0.1", recipient="User", message=user_message,
                                                    response=formatted_res)

                chatbot_response = format_bolden(chatbot_response)
    return JsonResponse({"message": "Simulation Done"})


def get_all_chats(request):
    chats = Conversation.objects.all().order_by("timestamp")
    chat_list = [
        {"sender": chat.sender, "recipient": chat.recipient, "user_query": chat.message, "AI_response": chat.response,
         "timestamp": chat.timestamp} for chat in chats]
    return JsonResponse({"chats": chat_list})


# format responses (like remove unicode) prior to saving it in DB
def format_response(text):
    return re.sub(r"[^\x00-\x7F]+", "", text)


# HTML/UI
def all_chats(request):
    chats = Conversation.objects.all().order_by("-timestamp")
    for chat in chats:
        chat.response = format_bolden(chat.response)

    return render(request, "chatbot/all_responses.html", {"chats": chats})


def chat_form(request):
    return render(request, "chatbot/fav_food_query.html")


def format_bolden(text):
    text = re.sub(r"\*\*(.*?)\*\*", r"<strong>\1</strong>", text)
    text = mark_safe(text)  # mark it safe
    return text

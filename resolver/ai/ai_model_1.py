# resolver/ai/ai_model_1.py
import ssl
import google.generativeai as genai
from .base_ai import BaseAI
from dotenv import load_dotenv
import os
load_dotenv()

class AIModel1(BaseAI):
    def __init__(self):
        super().__init__()
        api_key = os.getenv("GOOGLE_GENERATIVE_API_KEY")# Set up Google Generative AI API key
        genai.configure(api_key=api_key)
        ssl._create_default_https_context = ssl._create_stdlib_context

        # Set up GenerativeModel configuration
        self.generation_config = {
            "temperature": 1.2,
            "top_p": 1,
            "top_k": 1,
            "max_output_tokens": 2048,
        }

        self.safety_settings = [
            {"category": "HARM_CATEGORY_HARASSMENT", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
            {"category": "HARM_CATEGORY_HATE_SPEECH", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
            {"category": "HARM_CATEGORY_SEXUALLY_EXPLICIT", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
            {"category": "HARM_CATEGORY_DANGEROUS_CONTENT", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
        ]

        self.model = genai.GenerativeModel(
            model_name="gemini-1.0-pro", 
            generation_config=self.generation_config, 
            safety_settings=self.safety_settings
        )

    def process_message(self, message):
        # Determine if the message requests a microservice
        service_triggered = self.check_for_service(message)
        service_info = self.get_service_info(service_triggered) if service_triggered else "Tonoic provides exceptional services across all domains."

        # Construct the prompt
        prompt_parts = [
            "You are a dedicated AI assistant, like a friendly and professional waiter,\n",
            "who helps users with their needs in a polite and encouraging manner.\n",
            "You are here to teach them about Tonoic and its services,\n",
            "highlighting that Tonoic has the best expertise in the industry.\n",
            "{}\n".format(service_info),
            "User message: {}\n".format(message),
            "Your response (max 40 characters):\n"
        ]
        prompts = "".join(prompt_parts)
        
        # Generate the response from the model
        response = self.model.generate_content(prompts)
        
        # Extract the AI response text
        ai_response = response._result.candidates[0].content.parts[0].text
        
        # Ensure the response is a complete sentence
        ai_response = self.complete_sentence(ai_response)

        task_response = None
        if service_triggered:
            task_response = self.initiate_microservice(service_triggered)

        return {"ai_response": ai_response, "task": task_response}

    def complete_sentence(self, text):
        if '.' in text:
            return text[:text.rfind('.') + 1]
        return text[:40]  # Fallback in case there's no period

    def check_for_service(self, message):
        services = {
            "niche identification": "niche_identification",
            "branding": "branding",
            "landing page": "landing_page",
            "lead generation": "lead_gen",
            "closing": "closing",
            "advertisement campaign": "ad_campaign"
        }
        for key, value in services.items():
            if key in message.lower():
                return value
        return None

    def get_service_info(self, service_name):
        service_descriptions = {
            "niche_identification": "Our niche identification service helps you find specific niches relative to your location and generates an Ideal Customer Profile (ICP).",
            "branding": "Our branding service helps you find an unregistered, highly-brandable name and provides basic branding guidelines.",
            "landing_page": "Our landing page service creates template-based landing pages optimized for conversions and basic SEO.",
            "lead_gen": "Our lead generation service gathers leads from publicly available data and sets up automated email campaigns with personalized templates.",
            "closing": "Our closing service generates standard contracts with customizable templates and sets ideal contract pricing based on industry standards.",
            "ad_campaign": "Our advertisement campaign service sets up and manages marketing campaigns on major platforms and streamlines appointment scheduling."
        }
        return service_descriptions.get(service_name, "Tonoic provides exceptional services across all domains.")

    def initiate_microservice(self, service_name):
        services = {
            "niche_identification": self.niche_identification,
            "branding": self.branding,
            "landing_page": self.landing_page,
            "lead_gen": self.lead_gen,
            "closing": self.closing,
            "ad_campaign": self.ad_campaign
        }
        return services.get(service_name, lambda: f"Microservice {service_name} not found.")()

    def niche_identification(self):
        return "Niche Identification Service initiated. We will help you find a specific niche relative to your location and generate an Ideal Customer Profile (ICP)."

    def branding(self):
        return "Branding Service initiated. We will help you find an unregistered, highly-brandable name and provide basic branding guidelines."

    def landing_page(self):
        return "Landing Page Service initiated. We will create a template-based landing page optimized for conversions and basic SEO."

    def lead_gen(self):
        return "Lead Generation Service initiated. We will gather leads from publicly available data and set up automated email campaigns with personalized templates."

    def closing(self):
        return "Closing Service initiated. We will generate standard contracts with customizable templates and set ideal contract pricing based on industry standards."

    def ad_campaign(self):
        return "Advertisement Campaign Service initiated. We will set up and manage marketing campaigns on major platforms and streamline appointment scheduling."


# daphne -p 8001 tonoic.asgi:application
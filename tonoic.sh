#!/bin/bash

# Set the project name
PROJECT_NAME="tonoic"

# Create the Django project
django-admin startproject $PROJECT_NAME

# Navigate to the project directory
cd $PROJECT_NAME

# Create a function to create a Django app and its additional files
create_django_app() {
  django-admin startapp $1
  cd $1
  touch tasks.py serializers.py consumers.py Dockerfile
  cd ..
}

# Create the resolver app
create_django_app "resolver"

# Create specific niche identification apps
cd $PROJECT_NAME
mkdir -p specific_niche_identification
cd specific_niche_identification
create_django_app "market_research_tool"
create_django_app "icp_generator"
cd ..

# Create branding apps
mkdir -p branding
cd branding
create_django_app "name_generator"
create_django_app "branding_guide"
cd ..

# Create landing page service apps
mkdir -p landing_page_service
cd landing_page_service
create_django_app "template_based_landing_pages"
create_django_app "basic_seo_optimization"
cd ..

# Create sales outreach and lead generation apps
mkdir -p sales_outreach_lead_gen
cd sales_outreach_lead_gen
create_django_app "lead_generation_tool"
create_django_app "automated_email_campaigns"
create_django_app "crm_integration"
cd ..

# Create closing apps
mkdir -p closing
cd closing
create_django_app "contract_generator"
create_django_app "pricing_guide"
create_django_app "service_outline"
cd ..

# Create advertisement campaigns apps
mkdir -p advertisement_campaigns
cd advertisement_campaigns
create_django_app "automated_campaign_setup"
create_django_app "appointment_setting"
cd ..

# Create Docker and requirements files at the project root
cd ..
touch docker-compose.yml Dockerfile requirements.txt

# Add the apps to the Django project settings
cd $PROJECT_NAME
sed -i "/INSTALLED_APPS = \[/ a \ \ \ \ 'resolver',\n    'specific_niche_identification.market_research_tool',\n    'specific_niche_identification.icp_generator',\n    'branding.name_generator',\n    'branding.branding_guide',\n    'landing_page_service.template_based_landing_pages',\n    'landing_page_service.basic_seo_optimization',\n    'sales_outreach_lead_gen.lead_generation_tool',\n    'sales_outreach_lead_gen.automated_email_campaigns',\n    'sales_outreach_lead_gen.crm_integration',\n    'closing.contract_generator',\n    'closing.pricing_guide',\n    'closing.service_outline',\n    'advertisement_campaigns.automated_campaign_setup',\n    'advertisement_campaigns.appointment_setting'," settings.py

# Navigate back to the original directory
cd ../..


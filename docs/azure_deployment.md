# Azure App Service Deployment Guide

## Prerequisites

1. Azure CLI installed
2. Azure subscription
3. Azure App Service plan
4. Application code ready in a Git repository

## Deployment Steps

### 1. Azure Portal Method

1. Go to [Azure Portal](https://portal.azure.com)
2. Create a new Web App:
   - Click "Create a resource"
   - Search for "Web App"
   - Click "Create"

3. Configure the Web App:
   - **Subscription**: Select your subscription
   - **Resource Group**: Create new or select existing
   - **Name**: Choose a unique name (e.g., fa-knowledge-bot)
   - **Publish**: Code
   - **Runtime stack**: Python 3.11
   - **Operating System**: Linux
   - **Region**: Select nearest region
   - **App Service Plan**: Select or create new (Basic B1 or higher recommended)

4. Configure Application Settings:
   - Go to Configuration > Application Settings
   - Add the following settings:
     ```
     AZURE_OPENAI_API_KEY=your_api_key
     AZURE_OPENAI_ENDPOINT=your_endpoint
     AZURE_OPENAI_API_VERSION=2024-02-15-preview
     AZURE_OPENAI_CHAT_DEPLOYMENT=gpt35turbo
     AZURE_OPENAI_EMBEDDING_DEPLOYMENT=embedding
     STREAMLIT_SERVER_PORT=8000
     ```

5. Configure Startup Command:
   - Go to Configuration > General settings
   - Set Startup Command to:
     ```
     python -m streamlit run app.py --server.port 8000 --server.address 0.0.0.0
     ```

### 2. Azure CLI Method

1. Login to Azure:
```bash
az login
```

2. Create Resource Group (if needed):
```bash
az group create --name fa-knowledge-bot-rg --location eastus
```

3. Create App Service Plan:
```bash
az appservice plan create --name fa-knowledge-bot-plan --resource-group fa-knowledge-bot-rg --sku B1 --is-linux
```

4. Create Web App:
```bash
az webapp create --resource-group fa-knowledge-bot-rg --plan fa-knowledge-bot-plan --name fa-knowledge-bot --runtime "PYTHON|3.11" --startup-file "startup.txt"
```

5. Configure App Settings:
```bash
az webapp config appsettings set --resource-group fa-knowledge-bot-rg --name fa-knowledge-bot --settings AZURE_OPENAI_API_KEY="your_api_key" AZURE_OPENAI_ENDPOINT="your_endpoint" AZURE_OPENAI_API_VERSION="2024-02-15-preview" AZURE_OPENAI_CHAT_DEPLOYMENT="gpt35turbo" AZURE_OPENAI_EMBEDDING_DEPLOYMENT="embedding" STREAMLIT_SERVER_PORT="8000"
```

6. Deploy from Git:
```bash
az webapp deployment source config --name fa-knowledge-bot --resource-group fa-knowledge-bot-rg --repo-url https://github.com/FieldAssist/fa_knowledge_bot.git --branch master --manual-integration
```

## Post-Deployment

1. Access your app at: `https://fa-knowledge-bot.azurewebsites.net`

2. Monitor the application:
   - Go to App Service > Monitoring
   - Check Application Insights
   - View logs in Log stream

3. Troubleshooting:
   - Check deployment logs in Deployment Center
   - View application logs in Log stream
   - Monitor resource usage in Metrics

## Important Notes

1. **Environment Variables**: 
   - Never commit sensitive values to source control
   - Use Azure Key Vault for sensitive information in production

2. **Scaling**:
   - Monitor resource usage
   - Enable auto-scaling if needed
   - Consider Premium v3 plan for better performance

3. **Security**:
   - Enable HTTPS only
   - Configure authentication if needed
   - Review network security rules

4. **Monitoring**:
   - Set up alerts for errors
   - Monitor response times
   - Track resource utilization

## Maintenance

1. **Updates**:
   - Use deployment slots for zero-downtime updates
   - Test in staging slot before production
   - Monitor after each deployment

2. **Backup**:
   - Enable automatic backups
   - Test restore procedures
   - Document recovery process

3. **Cost Management**:
   - Monitor resource usage
   - Set up budget alerts
   - Optimize app service plan

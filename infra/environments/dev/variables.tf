variable "project_ids" {
  type        = map(string)
  description = "Map of project IDs per workspace (environment)"
  # TODO: Reemplazar con tus IDs reales de GCP
  default = {
    dev  = "nelson-acosta-ob-dev"
    prod = "nelson-acosta-ob-prod"
  }
}

variable "gcp_region" {
  type        = string
  description = "Default GCP region for resources"
  default     = "us-east1"
}

variable "product_name" {
  type        = string
  description = "Product name (lowercase, hyphenated)"
  default     = "nelson-acosta-ob"
}

variable "team" {
  type        = string
  description = "Team that owns this product"
  # TODO: Setear con tu equipo de dominio
  default = "aiops"
}

# TODO: Agregar las variables que necesiten tus módulos.
# Por ejemplo:
# 
# variable "light_rag_location" {
#   type        = string
#   description = "Location for Light RAG resources"
#   default     = "us-east1"
# }
# 
# variable "genai_gateway_url" {
#   type        = string
#   description = "URL of the GenAI Gateway"
#   default     = "https://genai.cosmos.dev.appslatam.com"
# }

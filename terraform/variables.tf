variable "google_provider_configurations" {
  type = map(string)
  default = {
    credentials  = ""
    project_name = ""
    region       = ""
  }
}

variable "webhook_url" {
  type        = string
  description = "SlackのWebhook URLを指定する"
}

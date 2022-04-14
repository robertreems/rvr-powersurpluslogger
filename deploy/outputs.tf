output "workspace_id" {
    value = module.log_analytics_workspace.workspace_id
}

output "primary_shared_key" {
    value = module.log_analytics_workspace.primary_shared_key
    sensitive = true
}

output "secondary_shared_key" {
    value = module.log_analytics_workspace.secondary_shared_key
    sensitive = true
}

output "key_id"{
    value = module.service_principal.key_id
}

output "value" {
    value = module.service_principal.value
    sensitive = true
}

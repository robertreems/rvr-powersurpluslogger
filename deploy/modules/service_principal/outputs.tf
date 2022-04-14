output "key_id" {
    value = azuread_service_principal_password.myfirstprincipalpassword.key_id 
}

output "value" {
    value = azuread_service_principal_password.myfirstprincipalpassword.value
}
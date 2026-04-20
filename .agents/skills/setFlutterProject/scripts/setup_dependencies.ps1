# PowerShell script to install Universal Kit dependencies
param(
    [string]$ProjectRoot = ".",
    [ValidateSet("Bloc", "Riverpod")]
    [string]$StateManagement = "Bloc"
)


Push-Location $ProjectRoot

Write-Host "📦 Installing Universal Kit Dependencies..." -ForegroundColor Cyan

# State Management
if ($StateManagement -eq "Bloc") {
    Write-Host "Installing Bloc Dependencies: flutter_bloc, bloc, equatable..."
    flutter pub add flutter_bloc bloc equatable
    Write-Host "Installing Bloc Dev Dependencies: bloc_test..."
    flutter pub add --dev bloc_test
}
elseif ($StateManagement -eq "Riverpod") {
    Write-Host "Installing Riverpod Dependencies: flutter_riverpod, riverpod_annotation..."
    flutter pub add flutter_riverpod riverpod_annotation
    Write-Host "Installing Riverpod Dev Dependencies: riverpod_generator, riverpod_lint, custom_lint..."
    flutter pub add --dev riverpod_generator riverpod_lint custom_lint
}

# Core Dependencies (Navigation)
Write-Host "Installing Core Dependencies: go_router..."
flutter pub add go_router

# Dev Dependencies (Common)
Write-Host "Installing Common Dev Dependencies: very_good_analysis, build_runner..."
flutter pub add --dev very_good_analysis build_runner


# Formatter
Write-Host "Formatting code..."
dart format .

Write-Host "✅ Universal Kit Setup Complete!" -ForegroundColor Green

Pop-Location

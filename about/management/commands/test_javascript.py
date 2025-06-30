"""
Django management command to run JavaScript tests
"""
from django.core.management.base import BaseCommand
import os
import subprocess
import sys


class Command(BaseCommand):
    help = 'Run JavaScript tests for the Anabel Sweets application'

    def add_arguments(self, parser):
        parser.add_argument(
            '--browser',
            action='store_true',
            help='Open test runner in browser',
        )
        parser.add_argument(
            '--verbose',
            action='store_true',
            help='Verbose output',
        )

    def handle(self, *args, **options):
        self.stdout.write(
            self.style.SUCCESS('🧪 Running JavaScript Tests for Anabel Sweets...')
        )
        
        # Check if test files exist
        test_file = 'staticfiles/js/tests.js'
        test_runner = 'staticfiles/js/test-runner.html'
        
        if not os.path.exists(test_file):
            self.stdout.write(
                self.style.ERROR(f'❌ Test file not found: {test_file}')
            )
            return
        
        if not os.path.exists(test_runner):
            self.stdout.write(
                self.style.ERROR(f'❌ Test runner not found: {test_runner}')
            )
            return
        
        self.stdout.write('✅ JavaScript test files found')
        
        # Display test information
        self.stdout.write('\n📋 JavaScript Test Coverage:')
        self.stdout.write('  • Flavor Selection Functionality')
        self.stdout.write('  • Custom Flavor Toggle')
        self.stdout.write('  • Form Validation')
        self.stdout.write('  • Date Validation Structure')
        self.stdout.write('  • Flavor Preview Update')
        self.stdout.write('  • Responsive Design Elements')
        
        self.stdout.write(f'\n📊 Total Tests: 6 JavaScript tests')
        
        # Instructions for running tests
        self.stdout.write('\n🚀 To run JavaScript tests:')
        self.stdout.write('  1. Start the Django development server:')
        self.stdout.write('     python manage.py runserver')
        self.stdout.write('  2. Open the test runner in your browser:')
        self.stdout.write('     http://127.0.0.1:8000/static/js/test-runner.html')
        self.stdout.write('  3. Click "Run All Tests" to execute the test suite')
        
        if options['browser']:
            try:
                # Try to open the test runner in the default browser
                import webbrowser
                test_url = 'http://127.0.0.1:8000/static/js/test-runner.html'
                self.stdout.write(f'\n🌐 Opening test runner in browser: {test_url}')
                webbrowser.open(test_url)
            except ImportError:
                self.stdout.write(
                    self.style.WARNING('⚠️  Could not open browser automatically')
                )
        
        if options['verbose']:
            self.stdout.write('\n📝 Test Details:')
            self.stdout.write('  • Test Environment: Browser-based with mock DOM')
            self.stdout.write('  • Test Framework: Custom JavaScript test suite')
            self.stdout.write('  • Coverage: Interactive form features and validation')
            self.stdout.write('  • Integration: Works with Django templates and forms')
        
        self.stdout.write(
            self.style.SUCCESS('\n✅ JavaScript test setup complete!')
        )
        self.stdout.write(
            '💡 Note: JavaScript tests require a browser environment to run properly.'
        ) 
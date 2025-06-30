/**
 * JavaScript Tests for Anabel Sweets Django Application
 * Tests interactive features and client-side functionality
 */

// Mock DOM environment for testing
function setupTestEnvironment() {
    // Create test HTML structure
    document.body.innerHTML = `
        <div class="order-container">
            <form method="post" novalidate>
                <div class="form-group">
                    <select id="id_cake_flavor">
                        <option value="">Select a flavor</option>
                        <option value="chocolate">Chocolate</option>
                        <option value="strawberry">Strawberry</option>
                        <option value="tiramisu">Tiramisu</option>
                        <option value="oreo">Oreo</option>
                        <option value="lime">Lime</option>
                        <option value="dulce_de_leche">Dulce de Leche</option>
                        <option value="custom">Custom Flavor</option>
                    </select>
                    
                    <div class="flavor-preview">
                        <div class="flavor-option" data-flavor="chocolate">
                            <img src="/static/images/chocolate.jpg" alt="Chocolate">
                            <div>Chocolate</div>
                        </div>
                        <div class="flavor-option" data-flavor="strawberry">
                            <img src="/static/images/strawberry.jpg" alt="Strawberry">
                            <div>Strawberry</div>
                        </div>
                        <div class="flavor-option" data-flavor="tiramisu">
                            <img src="/static/images/tiramisu.jpg" alt="Tiramisu">
                            <div>Tiramisu</div>
                        </div>
                        <div class="flavor-option" data-flavor="oreo">
                            <img src="/static/images/oreo.jpg" alt="Oreo">
                            <div>Oreo</div>
                        </div>
                        <div class="flavor-option" data-flavor="lime">
                            <img src="/static/images/lime.png" alt="Lime">
                            <div>Lime</div>
                        </div>
                        <div class="flavor-option" data-flavor="dulce_de_leche">
                            <img src="/static/images/dulcedeleche.png" alt="Dulce de Leche">
                            <div>Dulce de Leche</div>
                        </div>
                    </div>
                </div>
                
                <div class="form-group" id="custom-flavor-group" style="display: none;">
                    <label for="id_custom_flavor_description">Custom Flavor Description:</label>
                    <textarea id="id_custom_flavor_description" name="custom_flavor_description"></textarea>
                </div>
                
                <div class="form-group">
                    <label for="id_customer_name">Customer Name:</label>
                    <input type="text" id="id_customer_name" name="customer_name" required>
                </div>
                
                <div class="form-group">
                    <label for="id_customer_email">Customer Email:</label>
                    <input type="email" id="id_customer_email" name="customer_email" required>
                </div>
                
                <div class="form-group">
                    <label for="id_event_date">Event Date:</label>
                    <input type="date" id="id_event_date" name="event_date" required>
                </div>
            </form>
        </div>
    `;
}

// Test suite for Order Form JavaScript functionality
class OrderFormTests {
    constructor() {
        this.testResults = [];
        this.passedTests = 0;
        this.totalTests = 0;
    }

    // Helper method to run tests
    runTest(testName, testFunction) {
        this.totalTests++;
        try {
            testFunction();
            this.testResults.push(`✅ PASS: ${testName}`);
            this.passedTests++;
        } catch (error) {
            this.testResults.push(`❌ FAIL: ${testName} - ${error.message}`);
        }
    }

    // Test flavor selection functionality
    testFlavorSelection() {
        const flavorSelect = document.getElementById('id_cake_flavor');
        const flavorOptions = document.querySelectorAll('.flavor-option');
        
        // Test initial state
        if (flavorSelect.value !== '') {
            throw new Error('Flavor select should be empty initially');
        }
        
        // Test clicking on flavor option
        const chocolateOption = document.querySelector('[data-flavor="chocolate"]');
        chocolateOption.click();
        
        if (flavorSelect.value !== 'chocolate') {
            throw new Error('Flavor select should update when clicking flavor option');
        }
        
        // Test that selected class is applied
        if (!chocolateOption.classList.contains('selected')) {
            throw new Error('Selected flavor option should have "selected" class');
        }
    }

    // Test custom flavor toggle functionality
    testCustomFlavorToggle() {
        const flavorSelect = document.getElementById('id_cake_flavor');
        const customFlavorGroup = document.getElementById('custom-flavor-group');
        
        // Test that custom flavor group is hidden initially
        if (customFlavorGroup.style.display !== 'none') {
            throw new Error('Custom flavor group should be hidden initially');
        }
        
        // Test showing custom flavor group
        flavorSelect.value = 'custom';
        flavorSelect.dispatchEvent(new Event('change'));
        
        if (customFlavorGroup.style.display !== 'block') {
            throw new Error('Custom flavor group should be visible when custom is selected');
        }
        
        // Test hiding custom flavor group
        flavorSelect.value = 'chocolate';
        flavorSelect.dispatchEvent(new Event('change'));
        
        if (customFlavorGroup.style.display !== 'none') {
            throw new Error('Custom flavor group should be hidden when non-custom is selected');
        }
    }

    // Test form validation
    testFormValidation() {
        const form = document.querySelector('form');
        const customerName = document.getElementById('id_customer_name');
        const customerEmail = document.getElementById('id_customer_email');
        const eventDate = document.getElementById('id_event_date');
        
        // Test required field validation
        if (!customerName.hasAttribute('required')) {
            throw new Error('Customer name should be required');
        }
        
        if (!customerEmail.hasAttribute('required')) {
            throw new Error('Customer email should be required');
        }
        
        if (!eventDate.hasAttribute('required')) {
            throw new Error('Event date should be required');
        }
        
        // Test email format validation
        if (customerEmail.type !== 'email') {
            throw new Error('Customer email should have email type');
        }
    }

    // Test date validation (minimum 3 days in future)
    testDateValidation() {
        const eventDate = document.getElementById('id_event_date');
        
        // Set date to tomorrow (should be invalid)
        const tomorrow = new Date();
        tomorrow.setDate(tomorrow.getDate() + 1);
        eventDate.value = tomorrow.toISOString().split('T')[0];
        
        // Trigger validation
        eventDate.dispatchEvent(new Event('change'));
        
        // Note: This would need server-side validation, but we can test the client-side structure
        if (!eventDate.hasAttribute('required')) {
            throw new Error('Event date should be required for validation');
        }
    }

    // Test flavor preview update
    testFlavorPreviewUpdate() {
        const flavorSelect = document.getElementById('id_cake_flavor');
        const flavorOptions = document.querySelectorAll('.flavor-option');
        
        // Test that all flavor options exist
        if (flavorOptions.length !== 6) {
            throw new Error('Should have 6 flavor options');
        }
        
        // Test changing flavor via select
        flavorSelect.value = 'strawberry';
        flavorSelect.dispatchEvent(new Event('change'));
        
        const strawberryOption = document.querySelector('[data-flavor="strawberry"]');
        if (!strawberryOption.classList.contains('selected')) {
            throw new Error('Strawberry option should be selected when flavor is changed');
        }
    }

    // Test responsive design elements
    testResponsiveElements() {
        const flavorPreview = document.querySelector('.flavor-preview');
        const flavorOptions = document.querySelectorAll('.flavor-option');
        
        // Test that flavor preview exists
        if (!flavorPreview) {
            throw new Error('Flavor preview container should exist');
        }
        
        // Test that all flavor options have images
        flavorOptions.forEach(option => {
            const img = option.querySelector('img');
            if (!img) {
                throw new Error('Each flavor option should have an image');
            }
            if (!img.hasAttribute('alt')) {
                throw new Error('Each flavor image should have alt text');
            }
        });
    }

    // Run all tests
    runAllTests() {
        console.log('🧪 Starting JavaScript Tests for Anabel Sweets...\n');
        
        this.runTest('Flavor Selection Functionality', () => this.testFlavorSelection());
        this.runTest('Custom Flavor Toggle', () => this.testCustomFlavorToggle());
        this.runTest('Form Validation', () => this.testFormValidation());
        this.runTest('Date Validation Structure', () => this.testDateValidation());
        this.runTest('Flavor Preview Update', () => this.testFlavorPreviewUpdate());
        this.runTest('Responsive Design Elements', () => this.testResponsiveElements());
        
        // Print results
        console.log('\n📊 Test Results:');
        this.testResults.forEach(result => console.log(result));
        console.log(`\n🎯 Summary: ${this.passedTests}/${this.totalTests} tests passed`);
        
        if (this.passedTests === this.totalTests) {
            console.log('🎉 All JavaScript tests passed!');
        } else {
            console.log('⚠️  Some tests failed. Please review the results above.');
        }
        
        return this.passedTests === this.totalTests;
    }
}

// Test runner function
function runJavaScriptTests() {
    setupTestEnvironment();
    const tests = new OrderFormTests();
    return tests.runAllTests();
}

// Export for use in other contexts
if (typeof module !== 'undefined' && module.exports) {
    module.exports = { OrderFormTests, runJavaScriptTests };
}

// Auto-run tests if this file is loaded in browser
if (typeof window !== 'undefined') {
    window.runJavaScriptTests = runJavaScriptTests;
    console.log('JavaScript test suite loaded. Run runJavaScriptTests() to execute tests.');
} 
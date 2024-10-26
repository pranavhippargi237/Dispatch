document.addEventListener('DOMContentLoaded', function() {
    // Add new job section
    document.getElementById('addJobSection').addEventListener('click', function() {
        const jobSections = document.getElementById('jobSections');
        const sectionCount = jobSections.children.length + 1;
        
        const template = document.querySelector('.job-section').cloneNode(true);
        template.querySelector('h3').textContent = `Job Section ${sectionCount}`;
        
        // Clear all inputs in the new section
        template.querySelectorAll('input, select').forEach(input => {
            input.value = '';
        });
        
        // Clear extra assignments, leaving only one
        const assignments = template.querySelector('.assignments');
        const firstAssignment = assignments.querySelector('.assignment').cloneNode(true);
        assignments.innerHTML = '';
        assignments.appendChild(firstAssignment);
        
        jobSections.appendChild(template);
        setupEventListeners(template);
    });
    
    // Function to set up event listeners for each job section
    function setupEventListeners(section) {
        // Add assignment within a job section
        section.querySelector('.addAssignment').addEventListener('click', function() {
            const assignmentsContainer = section.querySelector('.assignments');
            const newAssignment = assignmentsContainer.querySelector('.assignment').cloneNode(true);
            
            // Clear input values in the cloned assignment
            newAssignment.querySelectorAll('input, select').forEach(input => {
                input.value = '';
            });
            
            assignmentsContainer.appendChild(newAssignment);
        });

        // Optional: Handle removal of an assignment
        section.querySelectorAll('.removeAssignment').forEach(button => {
            button.addEventListener('click', function() {
                const assignment = this.closest('.assignment');
                if (assignment) {
                    assignment.remove();
                }
            });
        });
    }

    // Setup initial event listeners for existing sections
    document.querySelectorAll('.job-section').forEach(section => {
        setupEventListeners(section);
    });
});

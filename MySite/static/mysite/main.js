const toggleFormLinks = document.querySelectorAll('.toggle-form');
const loginForm = document.querySelector('.login-form');
const registerForm = document.querySelector('.register-form');

toggleFormLinks.forEach(link => {
  link.addEventListener('click', () => {
    if (loginForm.style.display === 'none') {
      loginForm.style.display = 'block';
      registerForm.style.display = 'none';
    } else {
      loginForm.style.display = 'none';
      registerForm.style.display = 'block';
    }
  });
});


// Fade-in animation for faculty cards on scroll
const facultyCards = document.querySelectorAll('.faculty-card');

function checkScroll() {
  const triggerBottom = window.innerHeight * 0.8;

  facultyCards.forEach(card => {
    const cardTop = card.getBoundingClientRect().top;

    if (cardTop < triggerBottom) {
      card.classList.add('show');
    } else {
      card.classList.remove('show');
    }
  });
}

window.addEventListener('scroll', checkScroll);


// Fade-in animation for course cards on scroll
const courseCards = document.querySelectorAll('.course-card');

function checkScroll() {
  const triggerBottom = window.innerHeight * 0.8;

  courseCards.forEach(card => {
    const cardTop = card.getBoundingClientRect().top;

    if (cardTop < triggerBottom) {
      card.classList.add('show');
    } else {
      card.classList.remove('show');
    }
  });
}

window.addEventListener('scroll', checkScroll);


// Add active class to current page in navigation
const currentPage = window.location.pathname;
const navigationLinks = document.querySelectorAll('.nav-links a');

navigationLinks.forEach(link => {
  if (link.getAttribute('href') === currentPage) {
    link.classList.add('active');
  }
});


//Faculty lecturers and course allocation
const lecturerList = document.querySelector('.lecturer-list');
const courseList = document.querySelector('.course-list');

lecturerList.addEventListener('change', allocateCourses);
courseList.addEventListener('change', allocateCourses);

function allocateCourses() {
  const selectedLecturers = Array.from(document.querySelectorAll('.lecturer-item input[type="checkbox"]:checked'));
  const selectedCourses = Array.from(document.querySelectorAll('.course-item input[type="checkbox"]:checked'));

  selectedLecturers.forEach(lecturer => {
    const allocatedCourses = lecturer.getAttribute('data-courses');
    const newAllocatedCourses = selectedCourses.map(course => course.getAttribute('data-course'));
    lecturer.setAttribute('data-courses', newAllocatedCourses.join(','));

    if (allocatedCourses) {
      const previouslyAllocatedCourses = allocatedCourses.split(',');
      const unallocatedCourses = previouslyAllocatedCourses.filter(course => !newAllocatedCourses.includes(course));

      unallocatedCourses.forEach(course => {
        const unallocatedCourse = document.querySelector(`.course-item input[data-course="${course}"]`);
        if (unallocatedCourse) {
          unallocatedCourse.checked = false;
        }
      });
    }
  });
}

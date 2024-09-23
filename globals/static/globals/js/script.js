document.addEventListener('DOMContentLoaded', function() {
    var textarea = document.getElementById('code');

    textarea.addEventListener('keydown', function(e) {
        if (e.key === 'Tab') {
            e.preventDefault();

            var start = this.selectionStart;
            var end = this.selectionEnd;

            this.value = this.value.substring(0, start) + '\t' + this.value.substring(end);

            this.selectionStart = this.selectionEnd = start + 1;
        }
    });
});


function expand(element){
    const navbar = document.querySelector('.distance ul');
    
    if(navbar.style.left === '25px'){
        navbar.style.left = '-100%';
    }
    else{
        navbar.style.left = '25px';
    }

    element.classList.toggle('cross');
}
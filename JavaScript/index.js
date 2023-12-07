$(document).ready(function(){
            $(".navbar__menu li a").click(function(){
                $(".navbar__menu li a").removeClass("active");
                $(this).addClass("active");
                sessionStorage.setItem('activeLink', $(this).attr('href'));
            });
            var activeLink = sessionStorage.getItem('activeLink');
            if (activeLink) {
                $(".navbar__menu li a[href='" + activeLink + "']").addClass("active");
            }
            $(".navbar__logo1 a").click(function(){
                $(".navbar__menu li a").removeClass("active");
                $("#home").addClass("active");
                sessionStorage.setItem('activeLink', $(this).attr('href'));
            });
            var activeLink = sessionStorage.getItem('activeLink');
            if (activeLink) {
                $(".navbar__menu li a[href='" + activeLink + "']").addClass("active");
            }
            
        });

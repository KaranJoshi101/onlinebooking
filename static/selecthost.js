// select-detail-hospital;

select_slot_btn = document.querySelector(".select-slot-btn");
select_detail_hospital = document.querySelector(".select-detail-hospital");
form_slot = document.querySelector("#form-slot");

select_slot_btn.addEventListener("click",()=>{
    select_detail_hospital.style.display = "none";
    form_slot.style.display = "block";

})
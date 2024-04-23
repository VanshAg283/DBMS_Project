// admin.js

document.addEventListener('DOMContentLoaded', () => {
    const totalCustomers = parseInt(document.getElementById('totalCustomers').innerText);
    const totalDesigners = parseInt(document.getElementById('totalDesigners').innerText);

    const customerProgress = document.getElementById('customerProgress');
    const designerProgress = document.getElementById('designerProgress');

    // Calculate progress percentage for customers
    const customerPercentage = (totalCustomers / 100) * 100;
    customerProgress.style.width = `${customerPercentage}%`;

    // Calculate progress percentage for designers
    const designerPercentage = (totalDesigners / 100) * 100;
    designerProgress.style.width = `${designerPercentage}%`;
});

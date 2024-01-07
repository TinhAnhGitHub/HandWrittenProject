var TinhAnh = false;

document.addEventListener('DOMContentLoaded', () =>{
    const canvas = document.getElementById('drawCanvas');
    const context = canvas.getContext('2d');
    const clearButton = document.getElementById('clearButton');
    const saveButton = document.getElementById('saveButt')
    let isDrawing = false;

   
 


    canvas.addEventListener('mousedown', startDrawing);
    canvas.addEventListener('mousemove', draw);
    canvas.addEventListener('mouseup', stopDrawing);
    canvas.addEventListener('mouseout', stopDrawing);

    context.fillStyle='black';
    context.fillRect(0,0,canvas.width,canvas.height);

    clearButton.addEventListener('click', clearCanvas)
    saveButton.addEventListener('click', sendCanvas)


    function startDrawing(e) {
        isDrawing = true;
        draw(e);
    }

    function draw(e) {
        // if (!isDrawing) return;

        // context.lineWidth = 10;
        // context.lineCap = 'round';
        // context.strokeStyle = 'White';

        // context.lineTo(e.clientX - canvas.offsetLeft, e.clientY - canvas.offsetTop);
        // context.stroke();
        // context.beginPath();
        // context.moveTo(e.clientX - canvas.offsetLeft, e.clientY - canvas.offsetTop);
        if(!isDrawing) return;


        const rect = canvas.getBoundingClientRect();
        const x = e.clientX - rect.left;
        const y = e.clientY - rect.top;

        context.lineWidth = 10;
        context.lineCap = 'round';
        context.strokeStyle = 'white';

        context.lineTo(x, y);
        context.stroke();
        context.beginPath();
        context.moveTo(x, y);

    }

    function stopDrawing() {
        isDrawing = false;
        context.beginPath();
    }

    





  


   

    
})

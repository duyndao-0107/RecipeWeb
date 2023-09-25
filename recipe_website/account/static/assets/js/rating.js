const one = document.getElementById('one')
const two = document.getElementById('two')
const three = document.getElementById('three')
const four = document.getElementById('four')
const five = document.getElementById('five')

const form = document.querySelector('.rate-form')
const confirmBox = document.getElementById('confirm-box')
const csrf = document.getElementsByName('csrfmiddlewaretoken')

console.log(form)
console.log(confirmBox)
console.log(csrf)

const handleStarSelect = (size) => {
    const children = form.children
    for(let i=0; i < children.length; i++){
        if(i <= size){
            children[i].classList.add('checked')
        }
        else{
            children[i].classList.remove('checked')
        }
    }
}

const handleSelect = (selection) => {
    switch(selection){
        case 'one': {
            // one.classList.add('checked')
            // two.classList.remove('checked')
            // three.classList.remove('checked')
            // four.classList.remove('checked')
            // five.classList.remove('checked')
            handleStarSelect(1)
            return
        }

        case 'two': {
            handleStarSelect(2)
            return
        }

        case 'three': {
            handleStarSelect(3)
            return
        }

        case 'four': {
            handleStarSelect(4)
            return
        }

        case 'five': {
            handleStarSelect(5)
            return
        }
    }
    
}

const getNumericValue = (stringValue) => {
    let numericValue;

    if(stringValue === 'one'){
        numericValue = 1
    }
    else if(stringValue === 'two'){
        numericValue = 2
    }
    else if(stringValue === 'three'){
        numericValue = 3
    }
    else if(stringValue === 'four'){
        numericValue = 4
    }
    else if(stringValue === 'five'){
        numericValue = 5
    }
    else{
        numericValue = 0
    }
    return numericValue
}

if(one){
    const arr=[one, two, three, four, five]

    arr.forEach(item => item.addEventListener('mouseover', (event) => {
        handleSelect(event.target.id)
    }))

    arr.forEach(item => item.addEventListener('click', (event) => {
        const val=event.target.id
        console.log(val)
        let isSubmit = false

        form.addEventListener('submit', e => {
            e.preventDefault()
            const id = e.target.id
            console.log(id)
            const val_num = getNumericValue(val)
            
            if(isSubmit){
                return
            }

            isSubmit = true

            $.ajax({
                type: 'POST',
                url: '/menu/rate/',
                data: {
                    'csrfmiddlewaretoken': csrf[0].value,
                    'el_id': id,
                    'val': val_num,
                },
                success: function(reponse){
                    console.log(reponse)
                    confirmBox.innerHTML = `<h1>Successfully rated with ${reponse.score}</h1>`
                },
                error: function(error){
                    console.log(error)
                    confirmBox.innerHTML = `<h1>Oops... Something went wrong</h1>`
                }
            })
        })
    }))
}

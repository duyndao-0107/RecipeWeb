const one = document.getElementById('one')
const two = document.getElementById('two')
const three = document.getElementById('three')
const four = document.getElementById('four')
const five = document.getElementById('five')

console.log(one)

const arr=[one, two, three, four, five]

const handleSelect = (selection) => {
    switch(selection){
        case 'one': {
            one.classList.add('checked')
            two.classList.remove('checked')
            three.classList.remove('checked')
            four.classList.remove('checked')
            five.classList.remove('checked')
        }
    }
    
}

arr.forEach(item => item.addEventListener('mouseover', (event) => {
    console.log(event.target.id)
}))
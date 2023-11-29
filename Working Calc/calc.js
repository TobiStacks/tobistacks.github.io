const $lis = document.querySelectorAll("ul li")
// add $[variable] when getting objects from the DOM (doc object model)

$lis.forEach((node) => {
    node.addEventListener("mousedown", function(e) {
        //when using preventDefault, animations may not work for links/lists -> remove it
        e.preventDefault
        const val = node.innerText.trim()
        const $result = document.querySelector(".results")
        const resText = $result.innerText.trim()
        
        if(resText == '0' || resText == 'undefined' || resText == 'Infinity') {
            $result.innerText = ''
        }

        if(val == '=') {
            let solution = eval(resText)
            $result.innerText = solution
            return true
        }

        if(val.toLowerCase() == 'c') {
            $result.innerText = ''
            return true
        }

        $result.append(val)
    })
})
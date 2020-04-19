var family = {
    aaron: {
      name: 'Aaron',
      age: 30
    },
    megan: {
      name: 'Megan',
      age: 40
    },
    aaliyah: {
      name: 'Aaliyah',
      age: 2
    }
  }
  
  var list = function(family) {
    for (var prop in family) {
      document.getElementById('aaron-family').innerHTML += '<li>' + prop + '</li>';
      console.log(prop);
    }
  }


  list(family);
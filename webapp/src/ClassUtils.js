export function Subclass(data) {
  this.data = data;

  this.getType = function() {
    return this.data['TYPE'];
  }
}

export function Class(data) {
  this.subclasses = {};
  data.forEach((subclass_data)=> {
    let subclass = new Subclass(subclass_data);
    if(this.subclasses[subclass.getType()] === undefined) {
      this.subclasses[subclass.getType()] = [];
    }
    this.subclasses[subclass.getType()].push(subclass);
  });
}


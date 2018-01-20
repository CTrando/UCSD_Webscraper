//import {Heap} from './Heap.js';

//console.log(new Heap());



const heap = require('./Heap.js');

var h = new heap.Heap();
h.add("b");
h.add("d");
h.add("c");
h.add("e");
h.add("a");
h.add("f");
h.print();

h.removeRoot();
h.print();

h.removeRoot();
h.print();


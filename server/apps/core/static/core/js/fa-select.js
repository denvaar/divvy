
class FontAwesomeSelect {
  
  constructor(select, opts={}, data=[]) {
    this.getOpts(opts);
    if (data) {
      select = this.jsonToSelect(select, data);
    }
    this.select = select;
    this.select.style.display = "none";
    this.isActive = false;
    // get the selected value, or default to the first <option>
    var defaultOption = this.select.querySelector('option[selected]');
    this.defaultOption = defaultOption || this.select.querySelector("option");
    this.selectedIndex = this.select.selectedIndex;
    if (!defaultOption) this.selectedIndex += 1;
    // build out the HTML structure
    this.makeStructure();
    // Define the options (list items with the data-option attrib)
    this.options = [].slice.call(
      this.customSelect.querySelectorAll("li[data-option]"));
    this.selectedOption = this.customSelect.querySelector("span.placeholder");
    this.selectedOption.style.height = this.selectedHeight;
    this.selectedOption.style.lineHeight = this.selectedHeight;
    // setup event listeners.
    this.createEvents();
  }

  getOpts(opts) {
    this.opts = opts;
    if (!this.opts.optionSize) this.opts.optionSize = "fa-lg";
    if (!this.opts.selectionSize) this.opts.selectionSize = "fa-lg";
    var widths = {
      "fa-lg": "50px",
      "fa-2x": "50px",
      "fa-3x": "70px",
      "fa-4x": "95px",
      "fa-5x": "115px"
    };
    var heights = {
      "fa-lg": "29px",
      "fa-2x": "42px",
      "fa-3x": "58px",
      "fa-4x": "74px",
      "fa-5x": "90px"
    };
    this.selectedHeight = heights[this.opts.selectionSize];
    this.iconWidth = widths[this.opts.optionSize];
    this.selectedIconWidth = widths[this.opts.selectionSize];
  }

  // TODO could be re-factored out of class
  hasParent(e, p) {
    if (!e) return false;
    var el = e.target||e.srcElement||e||false;
    while (el && el != p) {
      el = el.parentNode||false;
    }
    return (el!==false);
  }

  jsonToSelect(select, data) {
    var options = data.map((obj) => {
      var option = document.createElement("option");
      if (obj.value) {
        option.value = obj.value;
      }
      option.dataset.meta = obj.meta;
      option.text = obj.label;
      return option;
    });
    options.forEach((option) => {
      select.appendChild(option);
    });
    return select;
  }

  makeStructure() {
    var options = "";
    var renderListItem = (el) => {
      
      var value = el.value;
      var metaLabel = "";
      var label = el.textContent;

      // Grab the meta options.
      for (var key in el.dataset) {
        if (el.dataset.hasOwnProperty(key)) {
          metaLabel = `<i data-meta class="fa fa-${el.dataset[key]} 
                       ${this.opts.optionSize}"></i>`;
        }
      }

      return `<li data-option data-value=${value}>
            ${metaLabel}
            <span data-label>${label}</span>
            </li>`;
    };
    [].slice.call(this.select.children).forEach((el) => {
      var tag = el.tagName.toLowerCase();

      if (tag === "option" && el.hasAttribute("value")) {
        options += renderListItem(el);
      }
    });

    var dropdown = `<div class="custom-options"><ul>${options}</ul></div>`;
    this.customSelect = document.createElement("div");
    this.customSelect.tabIndex = this.select.tabIndex;
    this.customSelect.className = "custom-select";
    this.customSelect.innerHTML = `<span class="placeholder">${this.defaultOption.textContent}</span>` + dropdown;
    this.select.parentNode.appendChild(this.customSelect);
    this.customSelect.appendChild(this.select); // Finished HTML structure

    [].slice.call(this.customSelect.querySelectorAll("i[data-meta]")).forEach((el) => {
      el.style.width = this.iconWidth; 
    });

  }

  createEvents() {
    var self = this;

    this.selectedOption.addEventListener("click", () => {
      self.toggleSelected();
    });

    this.options.forEach((option, index) => {
      option.addEventListener("click", () => {
        self.selectedIndex = index;
        self.toggleSelected();
        self.changeSelection();
      });
    });

    
    document.addEventListener("click", (event) => {
      if (self.isActive && event.target !== self.customSelect &&
          !self.hasParent(event.target, self.customSelect)) {
        
        self.toggleSelected();
      }
    });


    // keyboard navigation events
    this.customSelect.addEventListener("keydown", (event) => {
      var keyCode = event.keyCode || event.which;
     
      var len = self.options.length - 1;

      switch (keyCode) {
        case 38: // up key
          event.preventDefault();
          if (self.selectedIndex <= 0) { self.selectedIndex = len; }
          else { self.selectedIndex--; }
          self.updateItemClass();
          break;
        case 40: // down key
          event.preventDefault();
          if (self.selectedIndex >= len) { self.selectedIndex = 0; }
          else { self.selectedIndex++;}
          self.updateItemClass();
          break;
        case 32: // space key
          event.preventDefault();
          self.toggleSelected();
          break;
        case 13: // enter key
          event.preventDefault();
          if (self.isActive) {
            self.toggleSelected();
            self.changeSelection();
          }
          break;
      }
    });

  }

  updateItemClass() {
    var oldOption = this.customSelect.querySelector('li.active-item');
    if (oldOption) oldOption.classList.remove('active-item');
    this.options[this.selectedIndex].classList.add('active-item');
  }

  changeSelection() {
    var option = this.options[this.selectedIndex];
    this.selectedOption.innerHTML = option.innerHTML;
    var meta = this.selectedOption.querySelector("[data-meta]")
    if (meta) {
      if (this.opts.selectionSize !== this.opts.optionSize) {
        meta.classList.add(this.opts.selectionSize);
        meta.classList.remove(this.opts.optionSize);
      }
      meta.style.width = this.selectedIconWidth;
    }
    this.select.value = option.dataset.value;
  }

  toggleSelected() {
    this.customSelect.querySelector("div.custom-options").classList.toggle(
      "active-menu");
    this.selectedOption.classList.toggle("placeholder-active");
    this.isActive = !this.isActive;  
   
    this.updateItemClass();
  }

}

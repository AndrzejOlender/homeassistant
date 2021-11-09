import{_ as e,j as t,e as i,o,T as c,k as n,l as a,p as r,r as l,n as s,m as d,b as u,q as h}from"./main-60575625.js";import"./c.386ba692.js";e([s("search-input")],(function(e,t){return{F:class extends t{constructor(...t){super(...t),e(this)}},d:[{kind:"field",decorators:[i()],key:"filter",value:void 0},{kind:"field",decorators:[i({type:Boolean,attribute:"no-label-float"})],key:"noLabelFloat",value:()=>!1},{kind:"field",decorators:[i({type:Boolean,attribute:"no-underline"})],key:"noUnderline",value:()=>!1},{kind:"field",decorators:[i({type:Boolean})],key:"autofocus",value:()=>!1},{kind:"field",decorators:[i({type:String})],key:"label",value:void 0},{kind:"method",key:"focus",value:function(){this.shadowRoot.querySelector("paper-input").focus()}},{kind:"field",decorators:[o("paper-input",!0)],key:"_input",value:void 0},{kind:"method",key:"render",value:function(){return c`
      <paper-input
        .autofocus=${this.autofocus}
        .label=${this.label||"Search"}
        .value=${this.filter}
        @value-changed=${this._filterInputChanged}
        .noLabelFloat=${this.noLabelFloat}
      >
        <slot name="prefix" slot="prefix">
          <ha-svg-icon class="prefix" .path=${n}></ha-svg-icon>
        </slot>
        ${this.filter&&c`
          <mwc-icon-button
            slot="suffix"
            @click=${this._clearSearch}
            title="Clear"
          >
            <ha-svg-icon .path=${a}></ha-svg-icon>
          </mwc-icon-button>
        `}
      </paper-input>
    `}},{kind:"method",key:"updated",value:function(e){e.has("noUnderline")&&(this.noUnderline||void 0!==e.get("noUnderline"))&&(this._input.inputElement.parentElement.shadowRoot.querySelector("div.unfocused-line").style.display=this.noUnderline?"none":"block")}},{kind:"method",key:"_filterChanged",value:async function(e){r(this,"value-changed",{value:String(e)})}},{kind:"method",key:"_filterInputChanged",value:async function(e){this._filterChanged(e.target.value)}},{kind:"method",key:"_clearSearch",value:async function(){this._filterChanged("")}},{kind:"get",static:!0,key:"styles",value:function(){return l`
      ha-svg-icon,
      mwc-icon-button {
        color: var(--primary-text-color);
      }
      mwc-icon-button {
        --mdc-icon-button-size: 24px;
      }
      ha-svg-icon.prefix {
        margin: 8px;
      }
    `}}]}}),t);const k=d((e,t)=>e.filter(e=>v(e.name).includes(v(t))||v(e.description).includes(v(t))||v(e.category).includes(v(t))||v(e.full_name).includes(v(t))||v(e.authors).includes(v(t))||v(e.domain).includes(v(t)))),v=d(e=>String(e||"").toLocaleLowerCase().replace(/-|_| /g,""));e([s("hacs-checkbox")],(function(e,t){return{F:class extends t{constructor(...t){super(...t),e(this)}},d:[{kind:"field",decorators:[i({attribute:!1})],key:"checked",value:void 0},{kind:"field",decorators:[i({attribute:!1})],key:"label",value:void 0},{kind:"field",decorators:[i({attribute:!1})],key:"id",value:void 0},{kind:"get",key:"_checkboxClass",value:function(){return{checkbox:!0,checked:this.checked}}},{kind:"method",key:"render",value:function(){return c`
      <div class="checkbox-container">
        <div class=${u(this._checkboxClass)} @click=${this._checkboxClicked}>
          <div class="value">${this.checked?"✔":""}</div>
        </div>
        <div class="label" @click=${this._checkboxClicked}>${this.label}</div>
      </div>
    `}},{kind:"method",key:"_checkboxClicked",value:function(){this.checked=!this.checked,this.dispatchEvent(new CustomEvent("checkbox-change",{detail:{id:this.id},bubbles:!0,composed:!0}))}},{kind:"get",static:!0,key:"styles",value:function(){return[h,l`
        .checkbox-container {
          display: flex;
          color: var(--hcv-text-color-primary);
          -webkit-user-select: none;
          -moz-user-select: none;
          -ms-user-select: none;
          user-select: none;
        }

        .label {
          line-height: 18px;
          opacity: var(--dark-primary-opacity);
          font-family: var(--paper-font-subhead_-_font-family);
          -webkit-font-smoothing: var(--paper-font-subhead_-_-webkit-font-smoothing);
          font-size: var(--paper-font-subhead_-_font-size);
          cursor: pointer;
        }

        .value {
          margin-left: 2px;
          color: var(--hcv-text-color-on-background);
        }

        .checkbox {
          cursor: pointer;
          height: 16px;
          width: 16px;
          font-size: 14px;
          margin-right: 8px;
          background-color: var(--primary-background-color);
          border: 1px solid var(--divider-color);
          border-radius: 4px;
          line-height: 16px;
        }

        .checkbox.checked {
          border-color: var(--accent-color);
          background-color: var(--accent-color);
        }
      `]}}]}}),t),e([s("hacs-filter")],(function(e,t){return{F:class extends t{constructor(...t){super(...t),e(this)}},d:[{kind:"field",decorators:[i({attribute:!1})],key:"filters",value:void 0},{kind:"field",decorators:[i({attribute:!1})],key:"hacs",value:void 0},{kind:"method",key:"firstUpdated",value:async function(){this.addEventListener("checkbox-change",e=>this._filterClick(e))}},{kind:"method",key:"render",value:function(){var e;return c`
      <div class="filter">
        ${null===(e=this.filters)||void 0===e?void 0:e.map(e=>c`
            <hacs-checkbox
              class="checkbox"
              .label=${this.hacs.localize("common."+e.id)||e.value}
              .id=${e.id}
              .checked=${e.checked||!1}
            />
            </hacs-checkbox>`)}
      </div>
    `}},{kind:"method",key:"_filterClick",value:function(e){const t=e.detail;this.dispatchEvent(new CustomEvent("filter-change",{detail:{id:t.id},bubbles:!0,composed:!0}))}},{kind:"get",static:!0,key:"styles",value:function(){return[h,l`
        .filter {
          display: flex;
          border-bottom: 1px solid var(--divider-color);
          align-items: center;
          font-size: 16px;
          height: 32px;
          line-height: 4px;
          background-color: var(--sidebar-background-color);
          padding: 0 16px;
          box-sizing: border-box;
        }

        .checkbox:not(:first-child) {
          margin-left: 20px;
        }
      `]}}]}}),t);const f="m 20.064849,22.306912 c -0.0319,0.369835 -0.280561,0.707789 -0.656773,0.918212 -0.280572,0.153036 -0.605773,0.229553 -0.950094,0.229553 -0.0765,0 -0.146661,-0.0064 -0.216801,-0.01275 -0.605774,-0.05739 -1.135016,-0.344329 -1.402827,-0.7588 l 0.784304,-0.516495 c 0.0893,0.146659 0.344331,0.312448 0.707793,0.34433 0.235931,0.02551 0.471852,-0.01913 0.637643,-0.108401 0.101998,-0.05101 0.172171,-0.127529 0.17854,-0.191295 0.0065,-0.08289 -0.0255,-0.369835 -0.733293,-0.439975 -1.013854,-0.09565 -1.645127,-0.688661 -1.568606,-1.460214 0.0319,-0.382589 0.280561,-0.714165 0.663153,-0.930965 0.331571,-0.172165 0.752423,-0.25506 1.166895,-0.210424 0.599382,0.05739 1.128635,0.344329 1.402816,0.7588 l -0.784304,0.510118 c -0.0893,-0.140282 -0.344331,-0.299694 -0.707782,-0.331576 -0.235932,-0.02551 -0.471863,0.01913 -0.637654,0.10202 -0.0956,0.05739 -0.165791,0.133906 -0.17216,0.191295 -0.0255,0.293317 0.465482,0.420847 0.726913,0.439976 v 0.0064 c 1.020234,0.09565 1.638757,0.66953 1.562237,1.460213 z m -7.466854,-0.988354 c 0,-1.192401 0.962855,-2.155249 2.15525,-2.155249 0.599393,0 1.179645,0.25506 1.594117,0.707789 l -0.695033,0.624895 c -0.235931,-0.25506 -0.561133,-0.401718 -0.899084,-0.401718 -0.675903,0 -1.217906,0.542 -1.217906,1.217906 0,0.66953 0.542003,1.217908 1.217906,1.217908 0.337951,0 0.663153,-0.140283 0.899084,-0.401718 l 0.695033,0.631271 c -0.414472,0.452729 -0.988355,0.707788 -1.594117,0.707788 -1.192395,0 -2.15525,-0.969224 -2.15525,-2.148872 z M 8.6573365,23.461054 10.353474,19.14418 h 0.624893 l 1.568618,4.316874 H 11.52037 L 11.265308,22.734136 H 9.964513 l -0.274192,0.726918 z m 1.6833885,-1.68339 h 0.580263 L 10.646796,21.012487 Z M 8.1089536,19.156932 v 4.297745 H 7.1461095 v -1.645131 h -1.606867 v 1.645131 H 4.5763876 v -4.297745 h 0.9628549 v 1.696143 h 1.606867 V 19.156932 Z M 20.115859,4.2997436 C 20.090359,4.159461 19.969198,4.0574375 19.822548,4.0574375 H 14.141102 10.506516 4.8250686 c -0.14665,0 -0.2678112,0.1020202 -0.2933108,0.2423061 L 3.690064,8.8461703 c -0.00651,0.01913 -0.00651,0.03826 -0.00651,0.057391 v 1.5239797 c 0,0.165789 0.133911,0.299694 0.2996911,0.299694 H 4.5762579 20.0711 20.664112 c 0.165781,0 0.299691,-0.133905 0.299691,-0.299694 V 8.8971848 c 0,-0.01913 0,-0.03826 -0.0065,-0.05739 z M 4.5763876,17.358767 c 0,0.184917 0.1466608,0.331577 0.3315819,0.331577 h 5.5985465 3.634586 0.924594 c 0.184911,0 0.331571,-0.14666 0.331571,-0.331577 v -4.744098 c 0,-0.184918 0.146661,-0.331577 0.331582,-0.331577 h 2.894913 c 0.184921,0 0.331582,0.146659 0.331582,0.331577 v 4.744098 c 0,0.184917 0.146661,0.331577 0.331571,0.331577 h 0.446363 c 0.18491,0 0.331571,-0.14666 0.331571,-0.331577 v -5.636804 c 0,-0.184918 -0.146661,-0.331577 -0.331571,-0.331577 H 4.9079695 c -0.1849211,0 -0.3315819,0.146659 -0.3315819,0.331577 z m 1.6578879,-4.852498 h 5.6495565 c 0.15303,0 0.280561,0.12753 0.280561,0.280564 v 3.513438 c 0,0.153036 -0.127531,0.280566 -0.280561,0.280566 H 6.2342755 c -0.1530412,0 -0.2805719,-0.12753 -0.2805719,-0.280566 v -3.513438 c 0,-0.159411 0.1275307,-0.280564 0.2805719,-0.280564 z M 19.790657,3.3879075 H 4.8569594 c -0.1530412,0 -0.2805718,-0.1275296 -0.2805718,-0.2805642 V 1.3665653 C 4.5763876,1.2135296 4.7039182,1.086 4.8569594,1.086 H 19.790657 c 0.153041,0 0.280572,0.1275296 0.280572,0.2805653 v 1.740778 c 0,0.1530346 -0.127531,0.2805642 -0.280572,0.2805642 z";export{k as f,f as h};

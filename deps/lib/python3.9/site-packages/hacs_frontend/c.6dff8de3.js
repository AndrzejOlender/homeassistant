import{_ as i,j as o,e,T as r,b as t,r as n,n as a}from"./main-60575625.js";i([a("hacs-chip")],(function(i,o){return{F:class extends o{constructor(...o){super(...o),i(this)}},d:[{kind:"field",decorators:[e()],key:"icon",value:void 0},{kind:"field",decorators:[e()],key:"value",value:void 0},{kind:"field",decorators:[e()],key:"url",value:void 0},{kind:"method",key:"render",value:function(){return r`
      <div
        class="chip ${t({pointer:void 0!==this.url})}"
        @tap=${this._openURL}
      >
        <div class="icon"><ha-svg-icon .path=${this.icon}></ha-svg-icon></div>
        <div class="value">${String(this.value)||""}</div>
      </div>
    `}},{kind:"method",key:"_openURL",value:function(i){i.stopPropagation(),void 0!==this.url&&window.open(this.url,"_blank","rel=noreferer")}},{kind:"get",static:!0,key:"styles",value:function(){return[n`
        .chip {
          background-color: var(--hcv-color-chip);
          height: 24px;
          color: var(--hcv-text-color-chip);
          max-width: fit-content;
          display: flex;
          border-radius: 50px;
          padding: 0 4px;
          box-shadow: 2px 2px 8px 1px rgba(0, 0, 0, 0.3);
        }
        .icon {
          margin: auto;
          color: var(--hcv-color-chip);
          height: 20px;
          width: 20px;
          line-height: 20px;
          text-align: center;

          margin-left: -2px;
          background-color: var(--hcv-text-color-chip);
          border-radius: 50px;
        }
        .value {
          width: max-content;
          margin: 2px 5px auto;
        }
        .pointer {
          cursor: pointer;
        }
        ha-svg-icon {
          --mdc-icon-size: 16px;
        }
      `]}}]}}),o);

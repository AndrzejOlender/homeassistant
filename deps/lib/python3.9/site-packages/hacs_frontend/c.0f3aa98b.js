import{_ as i,H as e,e as o,T as t,v as a,d as s,q as c,r as n,n as d}from"./main-60575625.js";import{c as l}from"./c.d3dbc78b.js";i([d("hacs-dialog")],(function(i,e){return{F:class extends e{constructor(...e){super(...e),i(this)}},d:[{kind:"field",decorators:[o({type:Boolean})],key:"hideActions",value:()=>!1},{kind:"field",decorators:[o({type:Boolean})],key:"scrimClickAction",value:()=>!1},{kind:"field",decorators:[o({type:Boolean})],key:"escapeKeyAction",value:()=>!1},{kind:"field",decorators:[o({type:Boolean})],key:"noClose",value:()=>!1},{kind:"field",decorators:[o()],key:"title",value:void 0},{kind:"method",key:"render",value:function(){return this.active?t` <ha-dialog
      ?open=${this.active}
      ?scrimClickAction=${this.scrimClickAction}
      ?escapeKeyAction=${this.escapeKeyAction}
      @closed=${this.closeDialog}
      ?hideActions=${this.hideActions}
      .heading=${this.noClose?this.title:l(this.hass,this.title)}
    >
      <div class="content scroll" ?narrow=${this.narrow}>
        <slot></slot>
      </div>
      <slot class="primary" name="primaryaction" slot="primaryAction"></slot>
      <slot class="secondary" name="secondaryaction" slot="secondaryAction"></slot>
    </ha-dialog>`:t``}},{kind:"method",key:"closeDialog",value:function(){this.active=!1,this.dispatchEvent(new CustomEvent("closed",{bubbles:!0,composed:!0}))}},{kind:"get",static:!0,key:"styles",value:function(){return[a,s,c,n`
        .content {
          overflow: auto;
        }
        ha-dialog {
          --mdc-dialog-max-width: var(--hacs-dialog-max-width, calc(100vw - 16px));
          --mdc-dialog-min-width: var(--hacs-dialog-min-width, 280px);
        }
        .primary {
          margin-left: 52px;
        }

        @media only screen and (min-width: 1280px) {
          ha-dialog {
            --mdc-dialog-max-width: var(--hacs-dialog-max-width, 990px);
          }
        }
      `]}}]}}),e);

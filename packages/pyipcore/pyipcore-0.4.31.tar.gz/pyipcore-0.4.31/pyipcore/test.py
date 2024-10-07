if_en = ""
else_en = ""
if en:
    if_en = "if(en) begin"
    else_en = f"end else begin\n\tout = {m}'d0;\nend"
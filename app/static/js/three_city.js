/*三级联动高校*/
window.onload=function(){
        var provinceArray = "";
        var provicneSelectStr = "";
        for(var i=0,len=province.length;i<len;i++){
            provinceArray = province[i];
            provicneSelectStr = provicneSelectStr + "<option value='"+provinceArray[0]+"'>"+provinceArray[1]+"</option>"
        }
        $("#province").html(provicneSelectStr);
        $("#province1").html(provicneSelectStr);

        var selectCity = $("#province").val();
        var selectCity = $("#province1").val();
        var citylist=city[selectCity];
        var cityArray = "";
        var citySelectStr = "";
        for(var i=0,len=citylist.length;i<len;i++){
            cityArray = citylist[i];
            citySelectStr = citySelectStr + "<option value='"+cityArray[0]+"'>"+cityArray[1]+"</option>"
        }
        $("#city").html(citySelectStr);
        $("#city1").html(citySelectStr);

        var selectschool = $("#city").val();
        var selectschool = $("#city1").val();
        var schoolUlStr = "";
        var schoolListStr = allschool[selectschool];
        for(var i=0,len=schoolListStr.length;i<len;i++){
            schoolUlStr = schoolUlStr + "<option >"+schoolListStr[i][2]+"</option>";
        }
        schoolUlStr = schoolUlStr + "<option value='999'>其它</option>";
        $("#school1").html(schoolUlStr);
        $("#school").html(schoolUlStr);
        //省切换事件
        $("#province").change(function(){
            var selectCity = $("#province").val();
            var citylist=city[selectCity];
            var cityArray = "";
            var citySelectStr = "";
            if(citylist!=null){
                for(var i=0,len=citylist.length;i<len;i++){
                    cityArray = citylist[i];
                    citySelectStr = citySelectStr + "<option value='"+cityArray[0]+"'>"+cityArray[1]+"</option>"
                }
            }

            $("#city").html(citySelectStr);
            $("#school1").show();
            $("#school2").hide();
            var selectschool = $("#city").val();
            var schoolUlStr = "";
            var schoolListStr = allschool[selectschool];
            for(var i=0,len=schoolListStr.length;i<len;i++){
                schoolUlStr = schoolUlStr + "<option >"+schoolListStr[i][2]+"</option>";
            }
            schoolUlStr = schoolUlStr + "<option value='999'>其它</option>";
            $("#school").html(schoolUlStr);
        });
        $("#province1").change(function(){
            var selectCity = $("#province1").val();
            var citylist=city[selectCity];
            var cityArray = "";
            var citySelectStr = "";
            if(citylist!=null){
                for(var i=0,len=citylist.length;i<len;i++){
                    cityArray = citylist[i];
                    citySelectStr = citySelectStr + "<option value='"+cityArray[0]+"'>"+cityArray[1]+"</option>"
                }
            }

            $("#city1").html(citySelectStr);
            $("#school1").show();
            $("#school2").hide();
            var selectschool = $("#city").val();
            var schoolUlStr = "";
            var schoolListStr = allschool[selectschool];
            for(var i=0,len=schoolListStr.length;i<len;i++){
                schoolUlStr = schoolUlStr + "<option >"+schoolListStr[i][2]+"</option>";
            }
            schoolUlStr = schoolUlStr + "<option value='999'>其它</option>";
            $("#school").html(schoolUlStr);
        });
        //切换城市事件
        $("#city").change(function(){
            $("#school1").show();
            $("#school2").hide();
            var selectschool = $("#city").val();
            var schoolUlStr = "";
            var schoolListStr = allschool[selectschool];
            for(var i=0,len=schoolListStr.length;i<len;i++){
                schoolUlStr = schoolUlStr + "<option >"+schoolListStr[i][2]+"</option>";
            }
            schoolUlStr = schoolUlStr + "<option value='999'>其它</option>";
            $("#school").html(schoolUlStr);
        });
        $("#city1").change(function(){
            $("#school1").show();
            $("#school2").hide();
            var selectschool = $("#city1").val();
            var schoolUlStr = "";
            var schoolListStr = allschool[selectschool];
            for(var i=0,len=schoolListStr.length;i<len;i++){
                schoolUlStr = schoolUlStr + "<option >"+schoolListStr[i][2]+"</option>";
            }
            schoolUlStr = schoolUlStr + "<option value='999'>其它</option>";
            $("#school1").html(schoolUlStr);
        });
        $("#school1").change(function(){
            if($("#school").val()=="999"){
                $("#school1").hide();
                $("#school2").show();
            }
        });
    };

function drawLine(ctx, startX, startY, endX, endY,color){
  ctx.save();
  ctx.strokeStyle = color;
  ctx.beginPath();
  ctx.moveTo(startX,startY);
  ctx.lineTo(endX,endY);
  ctx.stroke();
  ctx.restore();
}

function drawBar(ctx, upperLeftCornerX, upperLeftCornerY, width, height,color){
  ctx.save();
  ctx.fillStyle=color;
  ctx.fillRect(upperLeftCornerX,upperLeftCornerY,width,height);
  ctx.restore();
}

function calcLevels(maxValue) {
  var log10 = Math.log10(maxValue);
  var floorLog10 = Math.floor(log10);
  var baseLevel = Math.pow(10,floorLog10);
  var numLevels = Math.ceil(maxValue/baseLevel);
  var levels = [];
  for (var i = 0; i <= numLevels; i++) {
    levels[i] = baseLevel * i;
  }

  return levels;
}

function Normalizer(maxLevel, pixelHeight) {
  this.maxLevel = maxLevel;
  this.pixelHeight = pixelHeight;

  this.getHeight = function (val) {
    var relativeHeight = val/this.maxLevel;
    var absoluteHeight = Math.floor(relativeHeight * this.pixelHeight);

    return absoluteHeight;
  }
}

function numberWithCommas(x) {
  var parts = x.toString().split(".");
  return parts[0].replace(/\B(?=(\d{3})+(?!\d))/g, ",");
}

function Chart(amplitude, max_num_bars, canvas_id) {
  this.sizes = {};
  var sz = this.sizes;
  sz.bar_width = 100;
  sz.vert_pad = 40;
  sz.horz_pad = 70;
  sz.bar_pad = 50;

  sz.grid_height = 400;
  sz.grid_width = sz.bar_pad + max_num_bars * sz.bar_width + sz.bar_pad;

  this.chart = document.querySelector(canvas_id);
  var chrt = this.chart;
  chrt.height = sz.vert_pad + sz.grid_height + sz.vert_pad;
  chrt.width = sz.horz_pad + sz.grid_width + sz.horz_pad;

  this.ctx = chrt.getContext("2d");
  this.ctx.translate(0.5, 0.5);

  this.turnOver = function () {
    this.ctx.translate(0, this.chart.height);
    this.ctx.scale(1, -1);
  }

  this.turnOverBackLocal = function (y) {
      this.ctx.scale(1, -1);
      this.ctx.translate(0, - (2 * y));
  }

  this.turnOver();

  this.levels = calcLevels(amplitude);
  var lvls = this.levels;
  this.norm = new Normalizer(lvls[lvls.length - 1], sz.grid_height);

  this.px_levels = [];
  for (var lev in lvls) {
    this.px_levels[lev] = this.norm.getHeight(lvls[lev]);
  }

  this.drawGrid = function (color) {
    for (var lev in this.px_levels) {
      var y = this.px_levels[lev] + sz.vert_pad;
      drawLine(this.ctx, sz.horz_pad, y, sz.grid_width + sz.horz_pad , y, color);

      this.ctx.save();
      this.turnOverBackLocal(y);


      var level = lvls[lev];
      this.ctx.fillStyle = color;
      this.ctx.font = "bold 12px Arial";
      this.ctx.fillText(numberWithCommas(level), 0, y);
      this.ctx.restore();
    }
  }

  this.left_offset = sz.horz_pad + sz.bar_pad;

  this.addBar = function(blocks) {
    var bot_offset = sz.vert_pad;

    for (var block in blocks) {
      var px_height = this.norm.getHeight(blocks[block].height);
      drawBar(this.ctx, this.left_offset, bot_offset, sz.bar_width, px_height, blocks[block].color);

      this.ctx.save();
      this.turnOverBackLocal(bot_offset + px_height);

      this.ctx.fillStyle = "#ffffff";
      this.ctx.font = "bold 12px Arial";
      this.ctx.fillText(blocks[block].text, this.left_offset + 10, bot_offset + px_height + 14);
      this.ctx.restore();

      bot_offset += px_height;
    }

    this.left_offset += sz.bar_width;
  }

}

